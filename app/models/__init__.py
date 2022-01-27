from sqlalchemy import (
    Column, DateTime,
    Integer, String, Text, func, Boolean
)

from app.database import Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=True, default=func.utc_timestamp())
    updated_at = Column(
        DateTime,
        nullable=True,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )


class Todo(Base, BaseMixin):
    __tablename__ = "todo"

    content = Column(String(300))
    color = Column(String(12))
    done = Column(Boolean)

    def __repr__(self):
        return f"<Todo {self.id}>"
