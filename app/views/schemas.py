from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Esquemas para el ETL

class ExtractRequest(BaseModel):
    """Solicitud para extracción desde la API Disney."""
    cantidad: int = Field(..., gt=0, description="Cantidad de registros a extraer (mayor que 0)")


class ExtractResponse(BaseModel):
    """Respuesta del endpoint de extracción."""
    mensaje: str
    registros_guardados: int
    fuente: str
    status: int


class TransformResponse(BaseModel):
    """Respuesta del endpoint de transformación y carga."""
    mensaje: str
    registros_procesados: int
    tabla_destino: str
    status: int


class ResetResponse(BaseModel):
    """Respuesta del endpoint de limpieza total."""
    mensaje: str
    mongo_docs_eliminados: int
    mysql_rows_eliminadas: int
    status: int

    # Esquemas para Personajes Disney


class PersonajeBase(BaseModel):
    """Atributos compartidos de un personaje Disney."""
    id: int
    name: str = Field(..., max_length=200)
    films: List[str] = []
    tvShows: List[str] = []
    parkAttractions: List[str] = []
    allies: List[str] = []          
    enemies: List[str] = []         
    videoGames: List[str] = []      
    shortFilms: List[str] = []      
    imageUrl: Optional[str] = None


class PersonajeCreate(PersonajeBase):
    """Esquema usado para crear un nuevo personaje en MongoDB."""
    pass


class PersonajeRead(BaseModel):
    """Esquema usado para devolver datos de personajes a clientes."""
    id: int
    name: str
    films: List[str]
    tvShows: List[str]
    parkAttractions: List[str]
    allies: List[str]
    enemies: List[str]
    videoGames: List[str]
    shortFilms: List[str]
    imageUrl: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}