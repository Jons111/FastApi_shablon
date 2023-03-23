from typing import Union

from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    username: str
    status: Union[bool, None] = None

class WorkerLogin(BaseModel):
    username: str
    password:str

class UserCreate(UserBase):
    password: str
    roll_id: int
    phone_id: int

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class PhoneBase(BaseModel):
    number : str
    name:str


class PhoneCreate(PhoneBase):
    type_id: int


class PhoneOut(PhoneBase):
    id: int

    class Config:
        orm_mode = True


class TitleBase(BaseModel):
    name: str


class TitleOut(TitleBase):
    id: int

    class Config:
        orm_mode = True

class PartnerBase(BaseModel):
    name: str
    address: str
    balance: int

class PartnerCreate(PartnerBase):
    user_id: int
    phone_id: int


class TaminotBase(BaseModel):
    name: str
    quantity: int
    price: int

class TaminotCreate(TaminotBase):
    user_id: int
    partner_id: int


class StoreBase(BaseModel):
    name: str
    long: float
    lat: float

class StoreCreate(StoreBase):
    user_id: int


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: int
    trade_price: int

class ProductCreate(ProductBase):
    user_id: int
    partner_id: int
    store_id: int


class CustomerBase(BaseModel):
    name: str
    balance: int

class CustomerCreate(CustomerBase):
    roll_id: int
    phone_id: int
    store_id: int


class OrderBase(BaseModel):
    name: str
    price: int
    quantity:int

class OrderCreate(OrderBase):
    customer_id: int
    phone_id: int
    store_id: int


class SaleBase(BaseModel):
    name: str
    price: int
    quantity: int


class SaleCreate(SaleBase):
    order_id: int
    customer_id: int
    phone_id: int
    store_id: int


class ProfitBase(BaseModel):
    price: int
    comment:str=None

class ProfitCreate(ProfitBase):
    customer_id: int
    user_id: int


class ExpenseBase(BaseModel):
    price: int
    type:str
    comment: str = None


class ExpenseCreate(ExpenseBase):
    user_id: int


class WorkerLoginBase(BaseModel):
    username: str
    password: str
    roll_id: int

class Token(BaseModel):
    access_token = str
    token = str

class TokenData(BaseModel):
    id:Optional[str]=None