# from fastapi import APIRouter,HTTPException,Path,Depends,File, UploadFile,Form
# from database import SessionLocal,engine
# import os
# from sqlalchemy.orm import Session
# from pydantic import BaseModel, Field

# from fastapi_pagination import Page, add_pagination, paginate
# from typing import List

# import crud
# from starlette.responses import JSONResponse
# from models import User
# from schemas import UserSchema
# authRouter=APIRouter()
# session=SessionLocal(bind=engine)
# @authRouter.get('/')
# async def auth():
#     return "Auth router................"

# @authRouter.post('/users/create')
# async def create(request:UserSchema, db:Session=Depends(get_db)):
#     response= crud.create_user(db,request)
  
#     return response
