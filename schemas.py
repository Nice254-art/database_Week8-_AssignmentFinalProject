# schemas.py
from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

# Product
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: Decimal
    stock_qty: int
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    stock_qty: Optional[int]
    category_id: Optional[int]

class ProductOut(ProductBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Customer
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]

class CustomerOut(CustomerBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

# Order related
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)

class OrderCreate(BaseModel):
    customer_id: int
    shipping_address: Optional[str] = None
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    status: str
    total_amount: Decimal
    shipping_address: Optional[str]
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
