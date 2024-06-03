from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,LargeBinary,Boolean,ARRAY,Text,Float
from sqlalchemy.orm import relationship,Mapped

import datetime
from database import Base
import enum
from sqlalchemy import Enum




class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    INTRANSIT = "IN-TRANSIT"
    DELIVERED = "DELIVERED"
    REJECTED="REJECTED"



class PizzaSizes(enum.Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
class OrderUserRelation(Base):
    __tablename__='orderUserRelation'
    id=Column(Integer,primary_key=True,autoincrement=True)
    order_id=Column(ForeignKey("order.id"),nullable=False)
    user_id=Column(ForeignKey("user.id"),nullable=False)

class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(25),nullable=False,unique=True)
    email=Column(String,nullable=False,unique=True)
    phone_number=Column(String,nullable=False)
    user_type=  Column(
        String,nullable=True
    )
    
    password=Column(Text,nullable=True)
    address=Column(String,nullable=True)
    is_active=Column(Boolean,default=False)
    is_staff=Column(Boolean,default=False)
    payment=relationship("Payment",backref="user")

# order product relationship
class OrderItem(Base):
    __tablename__='orderItem'
    id=Column(Integer,primary_key=True,autoincrement=True)
    order_id=Column(ForeignKey("order.id"),nullable=False)
    product_id=Column(ForeignKey("product.id"),nullable=False)
    quantity=Column(Integer,default=1)
   
    

 

  
class Payment(Base):
    __tablename__='payment'
    id=Column(Integer,primary_key=True,autoincrement=True)
    bank_name=Column(String(25),nullable=False,)
    account_number=Column(String,nullable=False)
    ifsc_code=Column(String,nullable=False)
    user_id=Column(ForeignKey("user.id"),nullable=False)
    order=relationship("Order",backref="payment")

   
  

class Order(Base):
    

   
    __tablename__='order'
    id=Column(Integer,primary_key=True,autoincrement=True)

    order_status=  Column(
        Enum(OrderStatus),
    )
    coupon_code=Column(String,nullable=True)
    discount=Column(Float,nullable=True)
    payment_id=Column(ForeignKey('payment.id'))
    orderItems=relationship("OrderItem",backref="orders")
    
    user_id=Column(Integer,ForeignKey('user.id'))

   
    assignee_id=Column(Integer,ForeignKey('user.id'),nullable=True)
    user = relationship("User",backref="user_orders", foreign_keys=[user_id] )
    assignee = relationship("User",backref="assignee_orders", foreign_keys=[assignee_id] )
    # user = relationship("User",backref="orders",foreign_keys=user_id, primaryjoin=user_id==User.id)
    # assignee = relationship("User",  foreign_keys=assignee_id, primaryjoin=assignee_id==User.id )
    
    
    
   
    
   
    

# class ProductCategoryRelation(Base):
#     __tablename__='productCategoryRelation'
#     id=Column(Integer,primary_key=True,autoincrement=True)
#     productCategory_id=Column(ForeignKey("productCategory.id"),nullable=False)
#     product_id=Column(ForeignKey("product.id"),nullable=False)



class ProductCategory(Base):
    

   
    __tablename__='productCategory'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False,unique=True)
    image=Column(String,nullable=True)



class Product(Base):
    

   
    __tablename__='product'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    productCategory_id=Column(ForeignKey("productCategory.id"),nullable=False)
    size=Column(ARRAY(String),nullable=True)
    description=Column(String,nullable=True)
    tags=Column(ARRAY(String),nullable=True)
    toppings=Column(ARRAY(String),nullable=True)
    productCategory=relationship("ProductCategory",backref="product")
    orders=relationship("OrderItem",backref="product")
    orderItems=relationship("OrderItem",backref="products")
    image=Column(String,nullable=True)
   
    
   
