from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Identity,
    Index,
    Integer,
    Text,
    text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, Identity(always=True), primary_key=True)
    goal_name = Column(Text, nullable=False)
    record_start = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    record_end = Column(TIMESTAMP(timezone=True), nullable=True)

    actions = relationship(
        "Action",
        back_populates="goal",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            "record_end IS NULL OR record_end >= record_start",
            name="goals_record_range_chk",
        ),
    )


class Action(Base):
    __tablename__ = "actions"

    # The table has no PK in the DB, but the ORM needs one to identify rows,
    # so (goal_id, time) is declared as a composite key here.
    goal_id = Column(
        Integer, ForeignKey("goals.id", ondelete="CASCADE"), primary_key=True
    )
    time = Column(
        TIMESTAMP(timezone=True),
        primary_key=True,
        nullable=False,
        server_default=text("now()"),
    )

    goal = relationship("Goal", back_populates="actions")

    __table_args__ = (Index("actions_goal_id_time_idx", "goal_id", "time"),)


class DailyAction(Base):
    """Read-only mapping of the daily_actions view (created in init.sql)."""

    __tablename__ = "daily_actions"

    goal_name = Column(Text, primary_key=True)
    day_completed = Column(Date, primary_key=True)
