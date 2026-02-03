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