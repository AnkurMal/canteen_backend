from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
import user


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
