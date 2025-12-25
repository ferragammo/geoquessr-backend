from typing import List

from app.api.dto import Modes
from app.api.locations import location_router
from app.api.locations.db_requests import get_locations_obj
from app.api.locations.model import LocationModel
from app.core.wrappers import GeoguessrResponseWrapper


@location_router.get('/start-game/{mode}')
async def get_locations(
        mode: Modes,
        amountOfRounds: int
) -> GeoguessrResponseWrapper[List[LocationModel]]:
    locations = await get_locations_obj(amountOfRounds, mode)
    return GeoguessrResponseWrapper(data=locations)
