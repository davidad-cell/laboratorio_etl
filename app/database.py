from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import config

def get_mongo_client():
    """
    Conexión a MongoDB.
    Almacenamiento Datos Crudos
    """
    client = MongoClient(config.MONGO_URI)
    return client[config.MONGO_DB]



Base = declarative_base()

def get_mysql_engine():
    """
    Aquí se almacenan los datos transformados y limpios.
    """
    connection_string = (
        f"mysql+pymysql://{config.MYSQL_USER}:"
        f"{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}/"
        f"{config.MYSQL_DB}"
    )

    engine = create_engine(
        connection_string,
        echo=False  # pon True solo para debug
    )
    return engine


def get_mysql_session():
    """
    Crea una sesión de SQLAlchemy para operaciones CRUD
    en el Data Warehouse.
    """
    engine = get_mysql_engine()
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    return Session()