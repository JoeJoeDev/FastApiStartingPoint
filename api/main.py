from fastapi import FastAPI
from db import models
from db.database import Connection

import os,sys
from dotenv import load_dotenv
from routers import user, auth

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'api/.env'))

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return "hello world"


connection = Connection()
models.Base.metadata.create_all(connection.engine)