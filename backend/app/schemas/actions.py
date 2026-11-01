from datetime import datetime

from pydantic import BaseModel


class Action(BaseModel):
    goal_id: int
    time_entered: datetime


class TriggerAction(BaseModel):
    goal_id: int
