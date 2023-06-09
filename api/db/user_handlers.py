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