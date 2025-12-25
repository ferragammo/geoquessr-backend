import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.wrappers import GeoguessrResponseWrapper, ErrorGeoguessrResponse

def create_app() -> FastAPI:
    app = FastAPI()

    from app.api.users import user_router
    app.include_router(user_router, tags=["user"])

    from app.api.locations import location_router
    app.include_router(location_router, tags=["location"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_, exc):
        return GeoguessrResponseWrapper(
            data=None,
            successful=False,
            error=ErrorGeoguessrResponse(message=str(exc.detail))
        ).response(exc.status_code)

    @app.get("/")
    async def read_root():
        return {"report": "Hello world!"}

    return app
