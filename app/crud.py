from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import UploadFile,File,HTTPException,Depends,status
from models import User,Order,ProductCategory,Product,OrderItem,Payment
from schemas import UserSchema,OrderSchema,ProductCategorySchema,ProductCategoryResponse,ProductSchema,ProductResponse,OrderItemSchema,OrderItemResponse,ProductCategoryUpdate,ProductUpdateSchema,UserUpdate,PaymentSchema,PaymentResponse,OrderUpdateSchema
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from typing import List
from datetime import datetime, timedelta
from typing import Annotated
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext




SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 890000

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# authentication


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow()+ timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token":encoded_jwt,
        "token_type": "bearer"
    }

def authenticate_user(db:Session,username:str,password:str):

    existing_user=db.query(User).filter(User.username==username).first()
    
    if existing_user is None:
        return HTTPException (status_code=400, detail="User does not Exist")
    elif verify_password(password,existing_user.password)== False:
        return HTTPException (status_code=400, detail="Unauthorized User")

    
    return create_access_token(data={"username":username,"password":password},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
   





def create_user(db:Session,user:UserSchema):
    existing_userEmail=db.query(User).filter(User.email==user.email).first()
    if existing_userEmail is not None:
        return HTTPException (status_code=400, detail="User Email Id Already Exist")
    existing_userName=db.query(User).filter(User.username==user.username).first()
    if existing_userName is not None:
        return HTTPException (status_code=400, detail="User Name Already Exist")

    user_res=User(username=user.username,email=user.email,password= get_password_hash(user.password)   ,is_active=user.is_active,is_staff=user.is_staff,phone_number=user.phone_number,address=user.address)
    db.add(user_res)
    db.commit()
    db.refresh(user_res)
    return user_res
def get_users(db:Session,username:str | None =None,is_staff:bool | None=False):
    if username is not None:
        return db.query(User).filter(User.username==username).all()
    
    if is_staff is not None:
        return db.query(User).filter(User.is_staff==True).all()


    return db.query(User).all()

def get_user_by_id(db:Session,user_id:int):
    print("userrdiddddd",user_id)
    user_res=db.query(User).filter(User.id==user_id).first()
    if user_res is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_res


# get_order_by_id
# 

def get_order_by_id(db:Session,order_id:int):
    
    order_res=db.query(Order).filter(Order.id==order_id).first()
    if order_res is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_res



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
   
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload",payload)
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    


# order============
def create_order(db:Session,order:OrderSchema):
    order_res=Order(**order.dict())
    db.add(order_res)
    db.commit()
    db.refresh(order_res)
    return order_res

def create_payment(db:Session,payment:PaymentSchema):
    
    

    payment_res=Payment(**payment.dict())
    db.add(payment_res)
    db.commit()
    db.refresh(payment_res)
    return payment_res
# get_allPayments
def get_allPayments(db:Session):
    return db.query(Payment).all()



def get_allOrders(db:Session,user_id:int| None=None,order_status:str| None =None,phone:str| None =None):
    
    if user_id is not None and order_status is not None:
        return db.query(Order).filter(Order.user_id==user_id,Order.order_status==order_status,Order.payment_id.isnot(None)).all()



    if user_id is not None:
        return db.query(Order).filter(Order.user_id==user_id,Order.payment_id.isnot(None)).all()
    if order_status is not None:
        return db.query(Order).filter(Order.order_status==order_status,Order.payment_id.isnot(None)).all()
    
    return db.query(Order).filter(Order.payment_id.isnot(None)).all()

# products=== category========
def create_category(db:Session,category:ProductCategorySchema):
   
    existing_category=db.query(ProductCategory).filter(ProductCategory.name==category.get("name")).first()
    if existing_category is not None:
       
        return HTTPException (status_code=400, detail="Product Category With this Name Already Exist")
   
  
    category_res=ProductCategory(**category)
    db.add(category_res)
    db.commit()
    db.refresh(category_res)
    return category_res
def get_category_by_id(db:Session,category_id:int):
    return db.query(ProductCategory).filter(ProductCategory.id==category_id).first()

def get_product_by_id(db:Session,id:int):
    return db.query(Product).filter(Product.id==id).first()

def update_category(db:Session,category:ProductCategoryUpdate,id:int):
    category_res=get_category_by_id(db=db,category_id=id)
    for key, value in category.items():
            setattr(category_res, key, value)
  
    db.commit()
    db.refresh(category_res)
    return category_res


def update_user(db:Session,user:UserUpdate,id:int):
    print("DattataUSerr",id,user)
    user_res=get_user_by_id(db=db,user_id=id)
    print("updateUser",user_res)
    if user_res is None:
        raise HTTPException(status_code=404, detail="User not found")
        


    for key, value in user.dict(exclude_unset=True).items():
        if value is not None:
            setattr(user_res, key, value)
                
            

            

    print("nullexclude",user_res)
  
    db.commit()
    db.refresh(user_res)
    return user_res
def update_order(db:Session,order:OrderUpdateSchema,id:int):
   
    order_res=get_order_by_id(db=db,order_id=id)
   
    if order_res is None:
        raise HTTPException(status_code=404, detail="Order not found")
        


    for key, value in order.dict(exclude_unset=True).items():
        if value is not None:
            setattr(order_res, key, value)
                
            

            

    
    db.commit()
    db.refresh(order_res)
    return order_res

def update_product(db:Session,product:ProductUpdateSchema,id:int):
    product_res=get_product_by_id(db=db,id=id)
    for key, value in product.items():
            
            if value is not None  :
                setattr(product_res, key, value)

           
  
    db.commit()
    db.refresh(product_res)
    return product_res



def get_matching_substring(main_string, substring):
    print("main_string",main_string,substring)
    index = main_string.find(substring)
    
    if index != -1:
        return main_string
    return ""



def get_allCategory(db:Session,search:str| None=None,category:str | None=None):
 
    if category is not None:
        
        filtered_category= db.query(ProductCategory).filter(func.lower(ProductCategory.name)== func.lower(category)).all()
        if search is not None:
            filtered_list=[]
            for categoryItems in filtered_category:
                
                if search.lower() in categoryItems.name.lower():

                    filtered_list.append(categoryItems)
            return filtered_list
            
        return filtered_category



    elif search is not None:

        return db.query(ProductCategory).filter(func.lower( ProductCategory.name).contains( func.lower(search))).all()
    return db.query(ProductCategory).all()
    


def create_product(db:Session,product:ProductSchema):
  
    product_res=Product(name=product.name,price=product.price,description=product.description,productCategory_id=product.productCategory_id,size=product.size,tags=product.tags,toppings=product.toppings)
    
    db.add(product_res)
    print("product_res22",product_res.size,product_res.tags,product_res.toppings)
    
    db.commit()
   
    db.refresh(product_res)
   
    return  product_res


def get_allProducts(db:Session,category_id:int | None=None,search:str|None=None):
    if category_id is not None:
        products_resp=db.query(Product).filter(Product.productCategory_id==category_id).all()
         
        if search is not None:
            filtered_list=[]
            for productItems in products_resp:
                
                if search.lower() in productItems.name.lower() or search.lower() in productItems.productCategory.name.lower():

                    filtered_list.append(productItems)
            return filtered_list
            
        return products_resp



    elif search is not None:

        return db.query(Product).filter(func.lower( Product.name).contains( func.lower(search))).all()
    return db.query(Product).all()
   
   

def create_OrderItem(db:Session,item:OrderItemSchema):
   
    product_res=OrderItem(product_id=item.product_id,order_id=item.order_id,quantity=item.quantity)
    
    db.add(product_res)
    
    db.commit()
   
    db.refresh(product_res)
   
    return  product_res


def get_allOrderItems(db:Session):
   
    return db.query(OrderItem).all()
