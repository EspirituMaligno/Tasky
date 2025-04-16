from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from enum import Enum
from datetime import datetime, timezone

Base = declarative_base()


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.TODO  # Важно: используем SQLEnum
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
