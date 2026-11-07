import pytz
from fastapi import APIRouter

from ..api.goals import Controller
from ..schemas.goals import GoalName, GoalStatus
from ..utils.logger import MyLogger

logger = MyLogger().get_logger()

con = Controller()

tz = pytz.timezone("Pacific/Auckland")

router = APIRouter()


@router.post("")
async def create_goal(goal: GoalName) -> None:
    return con.create_goal(goal)


@router.get("")
async def list_goals() -> list[GoalStatus]:
    return con.list_goals()
