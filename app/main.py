from typing import Union
from database import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from models import *
from routers import router
from database import SessionLocal
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
from jose import jwt
from passlib.context import CryptContext
app = FastAPI(docs_url="/docs")

app.mount("/uploadImage", StaticFiles(directory="uploadImage"), name="uploadImage")




origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,prefix="/api",tags=["apis"])
add_pagination(app)


@app.get("/")
async def home():
    return "welcome to pizza delivery app...."

