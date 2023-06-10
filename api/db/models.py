from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
from typing import List

class DBUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    #scopes=relationship('DBScopes', backref='scope')
    scopes: Mapped[List["DBScope"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class DBScope(Base):
    __tablename__ = "user_scope"
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    user_id: Mapped[int]  = mapped_column(ForeignKey('user.id'))
    user: Mapped["DBUser"] = relationship(back_populates='scopes')