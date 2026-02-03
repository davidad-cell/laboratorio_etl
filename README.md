# FastAPI ETL Disney Characters (MongoDB + MySQL)

Proyecto del curso Base de datos el cual tiene como objetivo desarrollar una aplicación de Ingeniería de Datos (Backend) que orqueste un proceso ETL
completo. El sistema expondrá tres endpoints en FastAPI: uno para la Ingesta (Staging), otro
para la Transformación y Carga (Warehouse), y un tercero para la Limpieza Total del
sistema.

El sistema extrae datos desde la [Disney API](https://api.disneyapi.dev/), los transforma para asegurar consistencia y los carga en MySQL, manteniendo idempotencia mediante UPSERT.

## Requisitos

- Python 3.10+ (recomendado 3.11)
- MongoDB en ejecución local 
- MySQL en ejecución local 

## Instalación y ejecución

1.  Crear entorno virtual e instalar dependencias:
   bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   

2.  Configurar variables de entorno:
   bash
   cp .env.example .env
   # Edita .env con tus credenciales de MySQL
   # Por defecto:
   MYSQL_USER=root
MYSQL_PASSWORD= password
MYSQL_HOST=localhost
MYSQL_DB=laboratorio_etl_db
    
     

3. Ejecutar el servidor:
   bash
   uvicorn app.main:app --reload
   
## Endpoints principales

- POST/api/v1/etl/extraer   → Extracción datos a MONGODB
- POST/api/v1/etl/transformar   → Transformación de datos, e imputación en MYSQL
- DELETE/api/v1/etl/reset   → Limpia los datos en MONGODB y vacia tabla MYSQL

Los Endpoints cumplen idempotencia y resilencia(Si la tabla no existe la aplicación debería crearla)