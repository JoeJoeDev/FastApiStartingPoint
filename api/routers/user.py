from typing import Annotated
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm.session import Session
from db.database import get_db
from routers.schema import User, UserDisplay
from db.user_handlers import add_user
from utils.oauth2 import get_current_user

import os

router = APIRouter(
    prefix="/user",
    tags=["user"],

)

@router.post("", response_model=UserDisplay)
def create_user(user: User, db: Session = Depends(get_db)):
   return add_user(db, user)

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Security(get_current_user, scopes=["items"])]):
    return current_user