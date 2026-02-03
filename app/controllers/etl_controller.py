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