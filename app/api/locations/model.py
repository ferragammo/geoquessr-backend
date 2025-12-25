from app.api.dto import Modes
from app.core.database import MongoBaseModel


class LocationModel(MongoBaseModel):
    mode: Modes
    latitude: float
    longitude: float