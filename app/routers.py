from fastapi import APIRouter,HTTPException,Path,Depends,File,Form,status,UploadFile
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

from database import SessionLocal,engine
import os
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from fastapi_pagination import paginate, Page, add_pagination
from typing import List
from typing import Annotated
import crud
from starlette.responses import JSONResponse
from models import User
from schemas import UserSchema,UserResponse,OrderSchema,OrderResponse,ProductCategorySchema,CategoryFilterSchema,ProductCategoryResponse,ProductSchema,ProductResponse,OrderItemSchema,OrderItemResponse,UserUpdate,PaymentSchema,PaymentResponse,OrderUpdateSchema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

router=APIRouter()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
session=SessionLocal(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")



# current user
# def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
#     print("get_current_user_token",token)
   
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username:str=payload.get("username")
#         password:str=payload.get("password")
#         print("payload",payload,username,password)
        
#     except JWTError as e:
#         print("JWTError",e)


#     user=db.query(User).filter(User.username==username).first()
#     print("userrr",user.username,user.id)
#     if user is None :
#         return {"message":"User Not Found"}
    

   
#     return user
def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    print("get_current_user_token",token)
   
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str=payload.get("username")
        password:str=payload.get("password")
        print("payload",payload,username,password)
        
    except JWTError as e:
        print("JWTError",e)


    user=db.query(User).filter(User.username==username).first()
    print("userrr",user.username,user.id)
    if user is None :
        return {"message":"User Not Found"}
    

   
    return user




@router.post('/auth/signup')
async def createUser(request:UserSchema, db:Session=Depends(get_db)):
    response= crud.create_user(db,request)
  
    return response

@router.get('/auth/allUsers',response_model=Page[UserResponse])
async def getUser(username:str | None =None,is_staff:bool| None=False, db:Session=Depends(get_db)):
    user_res= crud.get_users(db,username,is_staff)
    return paginate(user_res)

@router.get('/auth/user/{id}')
async def userById(id:int,db:Session=Depends(get_db)):
    user_res=  crud.get_user_by_id(db,id)
    return user_res


@router.patch("/auth/user/{id}", response_model=UserResponse)
async def update_user(id: str, user: UserUpdate,db:Session=Depends(get_db)):
    user_res=  crud.update_user(db,user,id)
    return user_res




@router.post('/auth/login')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)
):
    print("form_datalogin",form_data,form_data.username,form_data.password)
    user_res=  crud.authenticate_user(db,form_data.username,form_data.password)
    
    return user_res






# orders==================
@router.get('/order')
async def order():
    return "order router................"


# @router.post('/order/create')
# async def create_order(request:OrderSchema,
#     current_user: UserSchema=Depends(get_current_user),
#      db:Session=Depends(get_db)
    
# ):
   
#     if current_user.username:
#         print("current_user-orderrr",current_user)
        
#         response= crud.create_order( db,request,user_id=current_user.id)
#         return response


@router.post('/order/create')
async def create_order(request:OrderSchema,
    
     db:Session=Depends(get_db)
    
):
    if request.user_id is not None:
        response= crud.create_order( db,request)
        return response
    return HTTPException (status_code=400, detail="Plese Login yourself,user not found")

@router.patch("/order/update/{id}", response_model=OrderResponse)
async def update_order(id: str, order: OrderUpdateSchema,db:Session=Depends(get_db)):
    order_res=  crud.update_order(db,order,id)
    return order_res

@router.get('/order/allOrders',response_model=Page[OrderResponse])
async def getOrders(user_id:int| None = None,order_status:str| None=None,phone:str| None=None, db:Session=Depends(get_db)):
    user_res= crud.get_allOrders(db,user_id,order_status,phone)
    return paginate(user_res)
      
        
@router.get('/order/{id}',response_model=OrderResponse)
async def orderById(id:int,db:Session=Depends(get_db)):
    order_res=  crud.get_order_by_id(db,id)
    return order_res

    


# product category

@router.post('/category/create')
async def createCategory(name:str=File(...)  ,image:UploadFile=File(...), db:Session=Depends(get_db)):
    file_location=f"uploadImage/{image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
    # return {"info": f"file '{attachment.filename}' saved at '{file_location}'"}
    category={
        "name":name,
        "image":file_location,
       
    }
    response= crud.create_category(db,category)
  
    return response



@router.get('/category/detail/{id}',response_model=ProductCategoryResponse)
async def categoryById(id:int,db:Session=Depends(get_db)):
    category_res=  crud.get_category_by_id(db,id)
    return category_res

class CategoryFilter(Filter):
    order_by: Optional[list[str]]
@router.get('/category/allCategory',response_model=Page[ProductCategoryResponse])
async def getCategory(search: str | None = None,category:str| None=None, db:Session=Depends(get_db)):
    category_res= crud.get_allCategory(db,search,category)
    return paginate(category_res)


@router.patch('/category/update/{id}')
async def updateCategory(id:int,name:str =Form(...),image:UploadFile =File(...), db:Session=Depends(get_db)):
    file_location=f"uploadImage/{image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
   
    category={
        "id":id,
       
        "name":name,
       
        "image":file_location
    }
    print("taskIddd",id)
    category_res=  crud.update_category(db,category,id)
    return category_res

# products

@router.post('/product/create',response_model=ProductResponse)
async def createProduct(name:str =Form(...),price:float=Form(...),productCategory_id:int =Form(...),size:List =Form(...),description:str=Form(...),tags:List=Form(...),toppings:List=Form(...),image:UploadFile =File(...), db:Session=Depends(get_db)):
   
    file_location=f"uploadImage/{image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
  
    product={
        "name":name,
        "price":price,
        "productCategory_id":productCategory_id,
        "size":size,
        "description":description,
        "tags":tags,
        "toppings":toppings,

       
        "image":file_location
       
    }
    response= crud.create_product(db,product)
  

  
    return response

@router.get('/product/allProduct',response_model=Page[ProductResponse])
async def getProduct(category_id:int | None = None,search: str | None = None,db:Session=Depends(get_db)):
    product_res= crud.get_allProducts(db,category_id,search)
    
    print("alllproduct_res",product_res)
    if product_res is not None:
        print("alllproduct_res111",product_res)

        return paginate(product_res)
    print("alllproduct_res222",product_res)
    return  HTTPException (status_code=400, detail="Product does not Exist")

    
    


@router.get('/product/detail/{id}',response_model=ProductResponse)
async def productById(id:int,db:Session=Depends(get_db)):
    product_res=  crud.get_product_by_id(db,id)
    return product_res


@router.patch('/product/update/{id}')
async def updateProduct(id:int, name:str =Form(None),price:float =Form(None),productCategory_id:int =Form(None),
    size:List  =Form(None),description:str =Form(None),tags:List =Form(None),
    toppings:List  =Form(None),image:UploadFile =File(None), db:Session=Depends(get_db)):
    product={
        "id":id,
       
        "name":name,
        "price":price,
        "productCategory_id":productCategory_id,
        "size":size,
        "description":description,
        "tags":tags,
        "toppings":toppings,

       
        # "image":file_location
    }
    
    if image is not None:
        file_location=f"uploadImage/{image.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(image.file.read())

        product.update({"image":file_location})


    print("product",product)
   
    

    product_res=  crud.update_product(db,product,id)
    return product_res

# orderItem
@router.post('/order/orderItems',response_model=OrderItemResponse)
async def createOrderItem(request:OrderItemSchema, db:Session=Depends(get_db)):
    print("createOrderItem",request)
    response= crud.create_OrderItem(db,request)
    print("responseProdict",response)
  
    return response

@router.get('/order/allOrderItems',response_model=Page[OrderItemResponse])
async def getProduct(  db:Session=Depends(get_db)):
    product_res= crud.get_allOrderItems(db)
    return paginate(product_res)


@router.post('/payment',response_model=PaymentResponse)
async def createPayment(request:PaymentSchema, db:Session=Depends(get_db)):
    response= crud.create_payment(db,request)
  
    return response

@router.get('/allPayments',response_model=Page[PaymentResponse])
async def getAllPayments(db:Session=Depends(get_db)):
    payment_res= crud.get_allPayments(db)
    return paginate(payment_res)

