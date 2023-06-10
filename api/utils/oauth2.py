from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.user_handlers import get_user_by_username
from pydantic import BaseModel, ValidationError


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
 
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

SECRET_KEY = '86ae6420055de299da8887e52e1a719a447ca058ec05e53b0f53320655a026b6'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt
 
def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  authenticate_value = "Bearer"
  
  if security_scopes.scopes:
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
  
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": authenticate_value},
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("username")
    if username is None:
      raise credentials_exception
    token_scopes = payload.get("scopes", [])
    token_data = TokenData(scopes=token_scopes, username=username)
  except (JWTError, ValidationError):
    raise credentials_exception
  user = get_user_by_username(db, username=username)
  if user is None:
    raise credentials_exception
  breakpoint()
  for scope in security_scopes.scopes:
    print(scope)
    if scope not in token_data.scopes:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
      )

  return user

