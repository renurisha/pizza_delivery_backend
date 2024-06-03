# from fastapi import APIRouter,HTTPException,Path,Depends,File, UploadFile,Form
# from database import SessionLocal,engine
# import os
# from sqlalchemy.orm import Session
# from pydantic import BaseModel, Field

# from fastapi_pagination import Page, add_pagination, paginate
# from typing import List

# from starlette.responses import JSONResponse
# orderRouter=APIRouter()
# session=SessionLocal(bind=engine)
# @orderRouter.get('/')
# async def order():
#     return "order router................"
