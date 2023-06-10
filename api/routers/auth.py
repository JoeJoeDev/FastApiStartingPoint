from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from db.database import get_db
from sqlalchemy.orm.session import Session
from db.user_handlers import get_user_by_username
from utils.hashing import Hash
from utils.oauth2 import create_access_token

router = APIRouter(
    tags=["auth"],

)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.username)

    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_Not_Found, detail="User not found")

    scopes = []
    for scope in user.scopes:
        scopes.append(scope.name)
  
    access_token = create_access_token(data={'username': user.username, 'sub': user.username, 'scopes': scopes})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }