import logging

import pytz
from sqlalchemy import text

from ..models.models import Goal
from ..schemas.goals import GoalName, GoalStatus
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

    @log
    def list_goals(self) -> list[GoalStatus]:
        """Active goals, flagged if completed at least once today (NZ time)."""
        query = text(
            """
            SELECT g.id,
                   g.goal_name,
                   EXISTS (
                       SELECT 1 FROM actions a
                       WHERE a.goal_id = g.id
                         AND (a.time AT TIME ZONE 'Pacific/Auckland')::date
                             = (now() AT TIME ZONE 'Pacific/Auckland')::date
                   ) AS completed
            FROM goals g
            WHERE g.record_end IS NULL
            ORDER BY g.id
            """
        )
        with self.get_session() as session:
            rows = session.execute(query).all()
        return [GoalStatus(id=r.id, name=r.goal_name, completed=r.completed) for r in rows]
