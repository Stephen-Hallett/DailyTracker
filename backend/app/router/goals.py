import pytz
from fastapi import APIRouter, HTTPException, Query

from ..api.goals import Controller
from ..schemas.goals import Goal
from ..utils.logger import MyLogger

logger = MyLogger().get_logger()

con = Controller()

tz = pytz.timezone("Pacific/Auckland")

router = APIRouter()


@router.post("")
async def create_goal(goal: Goal) -> None:
    return con.create_goal(goal)
