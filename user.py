from fastapi import APIRouter, HTTPException, status
from sqlmodel import Field, SQLModel, select

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
async def register_user(user: UserCreate, session: SessionDep):
    user_exits = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if user_exits is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username is already taken")

    hashed = password_hash.hash(user.password)
    user_db = User(username=user.username, hashed_password=hashed)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db
