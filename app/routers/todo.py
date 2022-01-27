from typing import List

from devtools import debug
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schema
from app import database
from app import models

router = APIRouter()


@router.get('/list', response_model=List[schema.Todo])
async def get_todo_list(
        page: int, rows: int,
        conn: Session = Depends(database.get_conn)
):
    debug(page, rows)
    offset = 0
    if page > 1:
        offset = (page - 1) * rows
    queryset = conn.query(models.Todo)
    return queryset.offset(offset).limit(rows).all()


# @router.get('/list/all', response_model=List[schema.Todo])
# async def get_todo_list(
#         conn: Session = Depends(database.get_conn)
# ):
#     return conn.query(models.Todo).all()


@router.get('/find', response_model=schema.Todo)
async def find_todo_by(
        id: int,
        conn: Session = Depends(database.get_conn)
):
    return conn.query(models.Todo).get(id)


@router.post('/create', response_model=schema.IDResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
        todo_create: schema.TodoCreate,
        conn: Session = Depends(database.get_conn)
):
    todo = models.Todo(**todo_create.dict())
    conn.add(todo)
    conn.commit()
    return todo


@router.patch('/modify', response_model=schema.IDResponse)
async def update_todo(
        todo_modify: schema.TodoModify,
        conn: Session = Depends(database.get_conn)
):
    todo = conn.query(models.Todo).filter_by(id=todo_modify.id).first()
    if todo:
        todo.content = todo_modify.content
        todo.done = todo_modify.done
        todo.color = todo_modify.color
        conn.commit()
        return todo
    raise HTTPException(404, f'NOT FOUND TODO => {todo_modify.id}')


@router.delete('/remove')
async def remove_todo_by(
        id: int,
        conn: Session = Depends(database.get_conn)
):
    todo = conn.query(models.Todo).get(id)
    debug(todo)
    if todo:
        conn.delete(todo)
        conn.commit()
        return {'id': todo.id}
    raise HTTPException(404, 'NOT FOUND TODO')
