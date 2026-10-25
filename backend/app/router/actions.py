import pytz
from fastapi import APIRouter, HTTPException, Query

from ..api.actions import Controller
from ..schemas.actions import Action
from ..utils.logger import MyLogger

logger = MyLogger().get_logger()

con = Controller()

tz = pytz.timezone("Pacific/Auckland")

router = APIRouter()


@router.post("")
async def submit_action(action: Action) -> None:
    return con.submit_action(action)
