from datetime import datetime

from pydantic import BaseModel


class Goal(BaseModel):
    id: int
    name: str
    record_start: datetime
    record_end: datetime


class GoalName(BaseModel):
    name: str
