from typing import List

from app.api.users import user_router
from app.api.users.db_requests import get_top_10_users_obj, get_user_by_nickname_obj, upsert_result_obj
from app.api.dto import Modes
from app.api.users.model import UserModel
from app.api.users.schemas import UpsertUserResultRequest
from app.core.wrappers import GeoguessrResponseWrapper


@user_router.get('/all/{mode}')
async def all_users(
        mode: Modes
) -> GeoguessrResponseWrapper[List[UserModel]] | GeoguessrResponseWrapper[List]:
    users = await get_top_10_users_obj(mode)
    return GeoguessrResponseWrapper(data=users)


@user_router.get('/{nickname}')
async def get_user_by_nickname(
        nickname: str,
) -> GeoguessrResponseWrapper[UserModel]:
    user = await get_user_by_nickname_obj(nickname, load_results=True)
    return GeoguessrResponseWrapper(data=user)


@user_router.post('/result')
async def upsert_user_result(
        request: UpsertUserResultRequest,
) -> GeoguessrResponseWrapper[UserModel]:
    user = await upsert_result_obj(request.nickname, request.mode, request.amountOfPoints)
    return GeoguessrResponseWrapper(data=user)