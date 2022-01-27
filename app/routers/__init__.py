from devtools import debug
from fastapi import APIRouter, Depends
from app.routers import todo

router = APIRouter()

router.include_router(
    todo.router,
    prefix="/todo",
    tags=["Todo"],
    # dependencies=[Depends(api_key_defender)]
)
