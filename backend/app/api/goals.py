import logging
import os

import pytz
from sqlalchemy import select

from ..utils.db import BaseDatabase
from ..utils.logger import MyLogger, log
from ..schemas.goals import Goal


class Controller(BaseDatabase):
    @log
    def __init__(self) -> None:
        super().__init__()
        self.logger: logging.Logger = MyLogger().get_logger()
        self.tz: pytz.BaseTzInfo = pytz.timezone("Pacific/Auckland")

    @log
    def create_goal(self, goal: Goal) -> None:
        with self.get_session() as session:
            session.add(Goal(**goal.model_dump()))
            session.commit()
    
    
