import logging

import pytz

from ..models.models import Goal
from ..schemas.goals import GoalName
from ..utils.db import BaseDatabase
from ..utils.logger import MyLogger, log


class Controller(BaseDatabase):
    @log
    def __init__(self) -> None:
        super().__init__()
        self.logger: logging.Logger = MyLogger().get_logger()
        self.tz: pytz.BaseTzInfo = pytz.timezone("Pacific/Auckland")

    @log
    def create_goal(self, goal: GoalName) -> None:
        with self.get_session() as session:
            session.add(Goal(goal_name=goal.name))
            session.commit()
