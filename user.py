from fastapi import APIRouter
from sqlmodel import Field, SQLModel

from database import SessionDep, password_hash


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: int | None = Field(None, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: int


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep):
    hashed = password_hash.hash(user.password)
    user_db = User(username=user.username, hashed_password=hashed)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db
