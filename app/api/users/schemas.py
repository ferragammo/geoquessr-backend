from pydantic import BaseModel

from app.api.users.dto import Modes


class UpsertUserResultRequest(BaseModel):
    nickname: str
    mode: Modes
    amountOfPoints: float