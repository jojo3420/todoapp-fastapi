from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IDResponse(BaseModel):
    id: int
    created_at: Optional[datetime]
    # updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    content: str
    color: Optional[str]
    done: bool = False


class TodoModify(TodoCreate):
    id: int


class Todo(TodoCreate):
    id: int

    class Config:
        orm_mode = True
