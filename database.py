from typing import Annotated
from fastapi import Depends
from pwdlib import PasswordHash
from sqlalchemy import create_engine
from sqlmodel import Session

database_url = "sqlite:///database.db"
connect_args = {"check_same_thread": False}

engine = create_engine(database_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
password_hash = PasswordHash.recommended()