from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from routers.schema import User, UserDisplay
from db.user_handlers import add_user
import os

router = APIRouter(
    prefix="/user",
    tags=["user"],

)

@router.post("", response_model=UserDisplay)
def create_user(user: User, db: Session = Depends(get_db)):
   return add_user(db, user)