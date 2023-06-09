from fastapi import HTTPException, status
from db.models import DBUser
from routers.schema import User
from sqlalchemy.orm.session import Session
from utils.hashing import Hash
def add_user(db: Session, request: User):

    new_user = DBUser(
        username = request.username,
        email = request.email,
        password = Hash.hash_password(request.password) # need to hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db:Session, username: str):
    user = db.query(DBUser).filter(DBUser.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_Not_Found, detail="User not found")

    return user