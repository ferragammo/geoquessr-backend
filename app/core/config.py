import os
import pathlib
from functools import lru_cache
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    DB_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_DB_URL")).Geoquessr


class DevelopmentConfig(BaseConfig):
    Issuer = "http://localhost:8000"
    Audience = "http://localhost:3000"

class ProductionConfig(BaseConfig):
    Issuer = ""
    Audience = ""

@lru_cache()
def get_settings() -> DevelopmentConfig | ProductionConfig:
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }
    config_name = os.getenv("FASTAPI_CONFIG", default="development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
