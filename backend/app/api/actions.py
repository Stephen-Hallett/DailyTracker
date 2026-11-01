import logging

import pytz

from ..models.models import Action
from ..schemas.actions import TriggerAction
from ..utils.db import BaseDatabase
from ..utils.logger import MyLogger, log


class Controller(BaseDatabase):
    @log
    def __init__(self) -> None:
        super().__init__()
        self.logger: logging.Logger = MyLogger().get_logger()
        self.tz: pytz.BaseTzInfo = pytz.timezone("Pacific/Auckland")

    @log
    def submit_action(self, action: TriggerAction) -> None:
        with self.get_session() as session:
            session.add(Action(goal_id=action.goal_id))
            session.commit()
