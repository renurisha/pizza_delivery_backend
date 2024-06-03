from pydantic import BaseModel,ValidationInfo,field_validator,EmailStr,root_validator
from typing import List,Optional
from fastapi import UploadFile,File,HTTPException
from fastapi.responses import FileResponse
import enum
from sqlalchemy import Enum

import os


class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True

class UserEnum(enum.Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    CUSTOMER = "CUSTOMER"

class UserSchema(BaseModel):
  
    username: str 
    email: str 
    phone_number:str 
    password:str
    user_type:UserEnum| None="CUSTOMER"
    is_active:bool | None
    is_staff:bool | None=False
    address:str | None
    class Config:
        orm_mode = True





class UserUpdate(BaseModel):
  
    username: str | None =None
    email: str | None=None
    phone_number:str | None=None
    password:str| None=None
    is_active:bool | None=None
    is_staff:bool | None=None
    address:str | None=None
    user_type:str | None=None
    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id:int | None
  
    username: str | None
    email: str | None
    phone_number:str | None
    password:str
    is_active:bool | None
    is_staff:bool | None
    address:str | None
    user_type:str | None=None
    class Config:
        orm_mode = True


class PaymentSchema(BaseModel):
  
    bank_name: str 
    account_number: str 
    ifsc_code:str 
   
    user_id:int

    class Config:
        orm_mode = True

class PaymentResponse(BaseModel):
    id:int
  
    bank_name: str 
    account_number: str 
    ifsc_code:str 
   
    user_id:int
    user:UserResponse | None
   

    class Config:
        orm_mode = True


# class LoginSchema(BaseModel):
   
#     username: str 
    
#     password:str
   
#     class Config:
#         orm_mode = True


# orders
class OrderSchema(BaseModel):
  
    
    order_status:str| None="PENDING"
    user_id:int
    payment_id:int
    coupon_code:str | None=None
    discount:float | None=0
    assignee_id:int | None=None
   
   
    class Config:
        orm_mode = True


class OrderUpdateSchema(BaseModel):
  
    
    order_status:str| None=None
    user_id:int| None =None
    payment_id:int | None=None
    coupon_code:str | None=None
    discount:float | None=0
    assignee_id:int | None=None
   
   
    class Config:
        orm_mode = True





def download_file(file_name: str):
    print("file_name",file_name)
    return "http://127.0.0.1:8000/" + file_name
# product category
class ProductCategorySchema(BaseModel):
   
    name: str
    image:str | None
    
class ProductCategoryUpdate(BaseModel):
   
    name: str | None
    image:str | None
    


class CategoryFilterSchema(BaseModel):
     name: str | None

class ProductCategoryResponse(BaseModel):
    id:int
    name: str
    image:str | None
    @field_validator('image')
    @classmethod
    def check_fileDownload(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            print("value",v)
            return download_file(v)
    class Config:
        orm_mode = True
        
# product

class ProductSchema(BaseModel):
    
    name: str
    price:float
    productCategory_id:int
    size:List[str]
    description:str
    tags:List[str] | None
    toppings:List[str] | None
    image:str | None
    class Config:
        orm_mode = True


class ProductUpdateSchema(BaseModel):
   
    size:List[str] | None
    
    tags:List[str] |None
    toppings:List[str] | None
    image:str | None
    
   

    class Config:
        orm_mode = True
class ItemResponse(BaseModel):
    id:int
    
    name: str
    price:float
    productCategory_id:int
    size:List[str]
    description:str
    tags:List[str] | None
    toppings:List[str] | None
    image:str | None
    @field_validator('image')
    @classmethod
    def check_fileDownload(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            print("value",v)
            return download_file(v)
   
    class Config:
        orm_mode = True
# orderItem schema
class OrderItemSchema(BaseModel):
    order_id:int
    product_id:int
    quantity:int


class OrderItemResponse(BaseModel):
    id:int
    order_id:int
    product_id:int
    quantity:int | None=0
    product:ItemResponse | None
    
# prodtccategory relation 


class ProductResponse(BaseModel):
    id:int
    
    name: str
    price:float
    productCategory_id:int
    size:List[str]
    description:str
    tags:List[str] | None
    toppings:List[str] | None
    productCategory:ProductCategoryResponse | None
    # orders:List[OrderItemResponse] | None
    image:str | None=None
    @field_validator('image')
    @classmethod
    def check_fileDownload(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            print("value",v)
            return download_file(v)
    class Config:
        orm_mode = True
        
class OrderResponse(BaseModel):
    id:int
  
    # quantity: int
    
    order_status:str| None="PENDING"
    user_id:int
    payment_id:int | None
    coupon_code:str | None
    discount:float | None
    payment:PaymentResponse | None
    assignee_id:int | None=None
    orderItems:List[OrderItemResponse] | None
    assignee:UserResponse | None=None
    
   
   
    class Config:
        orm_mode = True


