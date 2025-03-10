from typing import Annotated

from fastapi import HTTPException, Depends, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Users
from database import SessionLocal
from routers.auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)
    confirmed_new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users) \
        .filter(Users.id == user.get('id')) \
        .first()

    if user_model is not None:
        return user_model

    raise HTTPException(status_code=404, detail='User not found.')


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency,
                          user: user_dependency,
                          password_request: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users) \
        .filter(Users.id == user.get('id')) \
        .first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')

    hashed_new_password = bcrypt_context.hash(password_request.new_password)

    if not bcrypt_context.verify(password_request.current_password,
                                 user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='The current password do not match.')

    if password_request.new_password != password_request.confirmed_new_password:
        raise HTTPException(status_code=400, detail='The new passwords do not match.')

    user_model.hashed_password = hashed_new_password

    db.add(user_model)
    db.commit()


@router.put("/phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(db: db_dependency,
                          user: user_dependency,
                          phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users) \
        .filter(Users.id == user.get('id')) \
        .first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')

    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()
