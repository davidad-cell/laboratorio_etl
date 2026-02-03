from fastapi import FastAPI
from sqlalchemy import text
from app.controllers.etl_controller import router as etl_router
from app.database import get_mysql_engine, Base

def create_app() -> FastAPI:
    app = FastAPI(
        title="ETL Pipeline API - Disney",
        description="Laboratorio Final - Pipeline ETL con FastAPI, MongoDB y MySQL usando Disney API",
        version="1.0.0"
    )

    # Incluir rutas del controlador ETL con prefijo
    app.include_router(etl_router, prefix="/api/v1/etl", tags=["ETL"])

    @app.on_event("startup")
    async def on_startup() -> None:
        try:
            engine = get_mysql_engine()
            Base.metadata.create_all(bind=engine)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            print("Conexion iniciada")
        except Exception as e:
            print(f"Error en conexión : {e}")

    

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "etl-pipeline"}

    return app

app = create_app()