from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, status, Request, Depends

from app import database
from app import schema
from app import models
from app import routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTION", "GET", "POST", "DELETE", "PUT", "PATCH"],
    allow_headers={"*"},
)


@app.on_event("startup")
def startup():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    models.Base.metadata.create_all(bind=database.engine)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check(request: Request):
    host = request.client.host
    user_agent = request.headers.get('user-agent')
    return {"ip": host, 'user_agent': user_agent}


app.include_router(routers.router)
