from typing import List

from app.api.dto import Modes
from app.api.locations import location_router
from app.api.locations.db_requests import get_locations_obj, insert_location_obj
from app.api.locations.model import LocationModel
from app.core.wrappers import GeoguessrResponseWrapper


@location_router.get('/start-game/{mode}')
async def get_locations(
        mode: Modes,
        amountOfRounds: int
) -> GeoguessrResponseWrapper[List[LocationModel]]:
    locations = await get_locations_obj(amountOfRounds, mode)
    return GeoguessrResponseWrapper(data=locations)


@location_router.post('/location')
async def insert_location(
        mode: Modes,
        country: str,
        city: str,
        name: str,
        latitude: float,
        longitude: float,
) -> GeoguessrResponseWrapper[LocationModel]:
    location = await insert_location_obj(mode, latitude, longitude, name, country, city)
    return GeoguessrResponseWrapper(data=location)
