import logging

import pytz
from sqlalchemy import text

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

    @log
    def dailycount(self) -> int:
        """Count of completed goals today."""
        query = text(
            """
            SELECT count(*)
            FROM goals g
            WHERE g.record_end IS NULL
            AND EXISTS (
                SELECT 1 FROM actions a
                WHERE a.goal_id = g.id
                    AND (a.time AT TIME ZONE 'Pacific/Auckland')::date
                        = (now() AT TIME ZONE 'Pacific/Auckland')::date
            )
            """
        )
        with self.get_session() as session:
            count = session.execute(query).scalar_one()
        self.logger.info("dailycount=%s", count)
        return int(count)
