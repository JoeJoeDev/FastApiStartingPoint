
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class Connection:

    def __init__(self):
        connectionString = os.environ['DATABASE_URI']
        self.engine = create_engine(connectionString)
        self.session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.db = self.session()

def get_db():
    connection = Connection()
    try:
        yield connection.db
    finally:
        connection.db.close()    