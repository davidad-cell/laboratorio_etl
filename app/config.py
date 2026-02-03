from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()


class config:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB", "disney_staging")

    
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_DB = os.getenv("MYSQL_DB")

    
    DISNEY_API_URL = os.getenv(
        "DISNEY_API_URL",
        "https://api.disneyapi.dev/character"
    )