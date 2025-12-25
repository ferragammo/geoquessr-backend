from typing import List

from app.api.dto import Modes
from app.api.locations.model import LocationModel
from app.core.config import settings


async def get_locations_obj(amount_of_rounds: int, mode: Modes) -> List[LocationModel]:
    locations = await settings.DB_CLIENT.locations.aggregate([
        {"$match": {"mode": mode}},
        {"$sample": {"size": amount_of_rounds}}
    ]).to_list(length=amount_of_rounds)

    return [LocationModel.from_mongo(location) for location in locations]


async def insert_location_obj(mode: Modes, latitude: float, longitude: float) -> None:
    location = LocationModel(mode=mode, latitude=latitude, longitude=longitude)

    await settings.DB_CLIENT.locations.insert_one(location.to_mongo())


