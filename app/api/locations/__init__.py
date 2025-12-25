from fastapi.routing import APIRouter

location_router = APIRouter(
    prefix="/api/location", tags=["location"]
)

from . import views

