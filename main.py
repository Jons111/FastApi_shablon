from datetime import timedelta, datetime
from typing import Optional,Union

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError,jwt
from routers.title_router import router
from fastapi import FastAPI, Depends, HTTPException, status, Body
from passlib.context import CryptContext

from sqlalchemy.orm import sessionmaker

from routers import *
from models.user_model import *
from routers import *

from db.config import Base, engine, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, get_db
from schemas.basemodels import *

Base.metadata.create_all(bind=engine)

from models.user_model import *

app = FastAPI(
    title="Implementing Security",
    description="Project to implement security in FastAPI",
    version="1.0.0"
)
Session = sessionmaker(bind=engine)
session = Session()



@app.get('/')
async def home():
    return {"message":"Welcome"}



app.include_router(
    auth_router.router,
    prefix='/users',
    tags=['For user auth'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    router,
    prefix='/title',
    tags=['For titles '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    worker_router.router_worker,
    prefix='/worker',
    tags=['For workers '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    phone_router.router_phone,
    prefix='/phone',
    tags=['For phone numbers '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)


app.include_router(
    partner_router.router_partner,
    prefix='/partner',
    tags=['For partners '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    customer_router.router_customer,
    prefix='/customer',
    tags=['For customers'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

# app.include_router(
#     router,
#     prefix='/title',
#     tags=['For titles '],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )
#
# app.include_router(
#     worker_router.router_worker,
#     prefix='/worker',
#     tags=['For workers '],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )
#
# app.include_router(
#     phone_router.router_phone,
#     prefix='/phone',
#     tags=['For phone numbers '],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )
#
#
# app.include_router(
#     partner_router.router_partner,
#     prefix='/partner',
#     tags=['For partners '],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )
#
# app.include_router(
#     partner_router.router_partner,
#     prefix='/partner',
#     tags=['For partners '],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )