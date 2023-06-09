from pydantic import BaseModel


class UserDisplay(BaseModel): 
    username: str
    email: str
    class Config():
        orm_mode = True

class User(UserDisplay):
    password: str
