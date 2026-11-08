import pytz
from fastapi import APIRouter

from ..api.actions import Controller
from ..schemas.actions import TriggerAction
from ..utils.logger import MyLogger

logger = MyLogger().get_logger()

con = Controller()

tz = pytz.timezone("Pacific/Auckland")

router = APIRouter()


@router.post("")
async def submit_action(action: TriggerAction) -> None:
    return con.submit_action(action)


@router.get("/dailycount")
async def daily_count() -> int:
    return con.dailycount()
