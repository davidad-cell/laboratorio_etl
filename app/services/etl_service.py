import requests
import pandas as pd
from typing import Dict, Any
from pymongo import UpdateOne
from sqlalchemy import text
from sqlalchemy.dialects.mysql import insert
from app.database import get_mongo_client, get_mysql_engine
from app.models.personajes_sql import PersonajeDisney, Base

class ETLService:
    def __init__(self):
        self.api_url = "https://api.disneyapi.dev/character"
        self.mongo_db = get_mongo_client()
        self.mysql_engine = get_mysql_engine()
        self.collection_name = "personajes_raw"

    # Extracción con idempotencia estricta
    async def extraer_datos_api(self, cantidad: int) -> Dict[str, Any]:
        try:
            if cantidad <= 0:
                return {
                    "mensaje": "La cantidad debe ser mayor a 0",
                    "registros_guardados": 0,
                    "fuente": "Disney API",
                    "status": 400
                }

            collection = self.mongo_db[self.collection_name]

            # Siempre traer desde la primera página
            response = requests.get(f"{self.api_url}?page=1", timeout=30)
            response.raise_for_status()
            data = response.json()
            personajes = data.get("data", [])

            # Tomar solo la cantidad solicitada
            personajes = personajes[:cantidad]

            operaciones = []
            for personaje in personajes:
                personaje_id = personaje.get("_id") or personaje.get("id")
                operacion = UpdateOne(
                    {"_id": personaje_id},
                    {"$set": personaje},
                    upsert=True
                )
                operaciones.append(operacion)

            if operaciones:
                collection.bulk_write(operaciones)

            print(f"Extracción completada: {len(operaciones)} personajes")

            return {
                "mensaje": "Datos extraídos exitosamente (idempotente)",
                "registros_guardados": len(operaciones),
                "fuente": "Disney API",
                "status": 201
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión con la API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error en extracción: {str(e)}")

    # Transformación y Carga con UPSERT
    async def transformar_cargar_datos(self) -> Dict[str, Any]:
        try:
            collection = self.mongo_db[self.collection_name]
            datos_mongo = list(collection.find({}))

            if not datos_mongo:
                return {
                    "mensaje": "No hay datos en MongoDB para transformar",
                    "registros_procesados": 0,
                    "tabla_destino": "personajes_master",
                    "status": 200
                }

            print(f"Datos en MongoDB: {len(datos_mongo)} documentos")

            df = pd.DataFrame(datos_mongo)

            # Asegurar columnas
            for col in ['films', 'tvShows', 'parkAttractions', 'allies', 'enemies', 'videoGames', 'shortFilms']:
                if col not in df.columns:
                    df[col] = ""

            # Renombrar _id a id si es necesario
            if "_id" in df.columns and "id" not in df.columns:
                df = df.rename(columns={"_id": "id"})

            # Convertir listas a strings
            def list_to_str(x):
                return ", ".join(x) if isinstance(x, list) else str(x) if x else ""

            for col in ['films', 'tvShows', 'parkAttractions', 'allies', 'enemies', 'videoGames', 'shortFilms']:
                df[col] = df[col].apply(list_to_str)

            columnas_finales = [
                'id', 'name', 'imageUrl',
                'films', 'tvShows', 'parkAttractions',
                'allies', 'enemies', 'videoGames', 'shortFilms'
            ]
            df_final = df[columnas_finales].fillna("")

            for col in ['films', 'tvShows', 'parkAttractions', 'allies', 'enemies', 'videoGames', 'shortFilms']:
                df_final[col] = df_final[col].apply(lambda x: "0" if str(x).strip() == "" else x)

            print(f"Datos transformados: {len(df_final)}")

            Base.metadata.create_all(self.mysql_engine)

            # UPSERT en MySQL
            with self.mysql_engine.connect() as conn:
                for _, row in df_final.iterrows():
                    stmt = insert(PersonajeDisney.__table__).values(
                        id=row['id'],
                        name=row['name'],
                        imageUrl=row['imageUrl'],
                        films=row['films'],
                        tvShows=row['tvShows'],
                        parkAttractions=row['parkAttractions'],
                        allies=row['allies'],
                        enemies=row['enemies'],
                        videoGames=row['videoGames'],
                        shortFilms=row['shortFilms']
                    )
                    stmt = stmt.on_duplicate_key_update(
                        name=stmt.inserted.name,
                        imageUrl=stmt.inserted.imageUrl,
                        films=stmt.inserted.films,
                        tvShows=stmt.inserted.tvShows,
                        parkAttractions=stmt.inserted.parkAttractions,
                        allies=stmt.inserted.allies,
                        enemies=stmt.inserted.enemies,
                        videoGames=stmt.inserted.videoGames,
                        shortFilms=stmt.inserted.shortFilms
                    )
                    conn.execute(stmt)
                conn.commit()

            registros_procesados = len(df_final)

            print(f"Transformación completada: {registros_procesados}")

            return {
                "mensaje": "Pipeline finalizado con UPSERT",
                "registros_procesados": registros_procesados,
                "tabla_destino": "personajes_master",
                "status": 200
            }

        except Exception as e:
            raise Exception(f"Error en transformación: {str(e)}")

    # Reset
    async def reset_sistema(self) -> Dict[str, Any]:
        try:
            collection = self.mongo_db[self.collection_name]
            mongo_count = collection.count_documents({})
            collection.delete_many({})

            with self.mysql_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT COUNT(*) as count FROM information_schema.tables "
                         "WHERE table_schema = DATABASE() AND table_name = 'personajes_master'")
                )
                table_exists = result.fetchone()[0] > 0

                mysql_count = 0
                if table_exists:
                    result = conn.execute(text("SELECT COUNT(*) as count FROM personajes_master"))
                    mysql_count = result.fetchone()[0]

                    conn.execute(text("TRUNCATE TABLE personajes_master"))
                    conn.commit()

            print(f"Sistema limpiado: MongoDB({mongo_count}), MySQL({mysql_count})")

            return {
                "mensaje": "Sistema reseteado correctamente",
                "mongo_docs_eliminados": mongo_count,
                "mysql_rows_eliminadas": mysql_count,
                "status": 200
            }

        except Exception as e:
            raise Exception(f"Error en reset: {str(e)}")
       