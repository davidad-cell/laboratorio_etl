from fastapi import APIRouter, HTTPException, status
from app.views.schemas import (
    ExtractRequest,
    ExtractResponse,
    TransformResponse,
    ResetResponse
)
from app.services.etl_service import ETLService

router = APIRouter(tags=["ETL"])
service = ETLService()

#Extracción Datos
@router.post(
    "/extraer",
    response_model=ExtractResponse,
    status_code=status.HTTP_201_CREATED
)
async def extraer_datos(request: ExtractRequest):
    try:
        resultado = await service.extraer_datos_api(cantidad=request.cantidad)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno durante la extracción: {str(e)}"
        )

#Transformación Datos
@router.post(
    "/transformar",
    response_model=TransformResponse,
    status_code=status.HTTP_200_OK
)
async def transformar_datos():
    try:
        resultado = await service.transformar_cargar_datos()
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno durante la transformación: {str(e)}"
        )

# =================================================
# Endpoint C: Reset del sistema
# =================================================
@router.delete(
    "/reset",
    response_model=ResetResponse,
    status_code=status.HTTP_200_OK
)
async def reset_sistema():
    try:
        resultado = await service.reset_sistema()
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno durante el reset del sistema: {str(e)}"
        )