from app.api.dto import Modes
from app.core.database import MongoBaseModel


class LocationModel(MongoBaseModel):
    name: str
    city: str
    country: str
    mode: Modes
    latitude: float
    longitude: float