import asyncio
from datetime import datetime
from typing import List
from fastapi import HTTPException

from app.api.dto import Modes
from app.api.users.model import UserModel, ResultsModel
from app.core.config import settings


async def get_top_10_users_obj(mode: Modes) -> List[UserModel] | List:
    results = await (settings.DB_CLIENT.results.find({"mode": mode})
                     .sort([("amountOfPoints", -1), ("datetimeUpdated", 1)])
                     .to_list(length=10))
    if not results:
        return []
    user_ids = [result["userId"] for result in results]

    users_data = await settings.DB_CLIENT.users.find(
        {"id": {"$in": user_ids}}
    ).to_list(length=None)

    results_models = [ResultsModel.from_mongo(result) for result in results]

    users = [UserModel.from_mongo(user) for user in users_data]
    UserModel.populate_results(users, results_models)

    return users


async def get_user_by_nickname_obj(nickname: str, load_results: bool = False) -> UserModel:
    user_data = await settings.DB_CLIENT.users.find_one({"nickname": nickname})
    if not user_data:
        return UserModel(nickname=nickname)

    user = UserModel.from_mongo(user_data)

    if not load_results or not user.results:
        return user

    results = await asyncio.gather(
        *[get_result_by_id_obj(result_id) for result_id in user.results]
    )

    return await user.load_results(results)


async def get_result_by_id_obj(result_id: str) -> ResultsModel | None:
    result = await settings.DB_CLIENT.results.find_one({"id": result_id})
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultsModel.from_mongo(result)


async def insert_user_obj(user: UserModel) -> None:
    await settings.DB_CLIENT.users.insert_one(user.to_mongo())


async def insert_result_obj(result: ResultsModel) -> None:
    await settings.DB_CLIENT.results.insert_one(result.to_mongo())


async def update_user_obj(user_id: str, result_id: str) -> None:
    await settings.DB_CLIENT.users.update_one(
        {"id": user_id},
        {"$push": {"results": result_id}}
    )


async def upsert_result_obj(nickname: str, mode: Modes, amount_of_points: float) -> UserModel:
    user = await get_user_by_nickname_obj(nickname)

    existing_result = None
    if user.results:
        existing_result = await settings.DB_CLIENT.results.find_one({
            "userId": user.id,
            "mode": mode
        })
    else:
        await insert_user_obj(user)

    if existing_result:
        await settings.DB_CLIENT.results.update_one(
            {"id": existing_result["id"]},
                {"$set":
                    {
                        "amountOfPoints": amount_of_points,
                        "datetimeUpdated": datetime.now()
                    }
                }
            )
    else:
        result = ResultsModel(
            userId=user.id,
            mode=mode,
            amountOfPoints=amount_of_points
        )

        asyncio.create_task(insert_result_obj(result))
        asyncio.create_task(update_user_obj(user.id, result.id))
        user.results.append(result.id)

    results = await asyncio.gather(
        *[get_result_by_id_obj(result_id) for result_id in user.results]
    )

    return await user.load_results(results)


