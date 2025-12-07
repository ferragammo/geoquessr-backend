import asyncio
from datetime import datetime
from typing import List

from pydantic import Field

from app.api.users.dto import Modes
from app.core.database import MongoBaseModel


class ResultsModel(MongoBaseModel):
    userId: str
    mode: Modes
    amountOfPoints: float = Field(default=0)
    datetimeUpdated: datetime = Field(default_factory=datetime.now)


class UserModel(MongoBaseModel):
    nickname: str
    results: List[str] | List[ResultsModel] = Field(default_factory=list)

    @classmethod
    def populate_results(cls, users: List['UserModel'], results: List[ResultsModel]) -> None:
        results_by_user_id = {}
        for result in results:
            if result.userId not in results_by_user_id:
                results_by_user_id[result.userId] = []
            results_by_user_id[result.userId].append(result)

        for user in users:
            user_id_str = str(user.id)
            if user_id_str in results_by_user_id:
                user.results = results_by_user_id[user_id_str]


    async def load_results(self, results: List[ResultsModel]) -> 'UserModel':
        self.results = [r for r in results if r is not None]

        return self


