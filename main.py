from datetime import timedelta, datetime
from typing import Optional,Union

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError,jwt

from fastapi import FastAPI, Depends, HTTPException, status, Body
from passlib.context import CryptContext

from sqlalchemy.orm import sessionmaker

import routers.auth_router
from models.user_model import *
from routers import auth_router, title_router

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

# For Titles
@app.post('/title/add', status_code=201)
def home(data: TitleBase, ):
    c1 = TitleModel(name=data.name)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.get('/title/',  status_code = 200)
def get_all_titles(db: Session = Depends(get_db)):
    titles = db.query(TitleModel).all()
    return {"data":titles}

@app.get('/title/{id}', status_code = 200)
def get_one_title(id:int ,db: Session = Depends(get_db)):
    titles = db.query(TitleModel).filter(TitleModel.id==id).all()
    return {"data":titles}

@app.patch('/title/{id}')
def update_title(id: int, payload:TitleBase ):
    note_query = session.query(TitleModel).filter(TitleModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(TitleModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}


# For Phones numbers
@app.post('/phone/add', )
def home(data: PhoneCreate, ):
    c1 = PhoneModel(type_id=data.type_id,number=data.number,name=data.name)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}
@app.get('/phone/',  status_code = 200)
def get_all_phones(db: Session = Depends(get_db)):
    titles = db.query(PhoneModel).all()
    return {"data":titles}

@app.get('/phone/{id}', status_code = 200)
def get_one_phone(id:int ,db: Session = Depends(get_db)):
    titles = db.query(PhoneModel).filter(PhoneModel.id==id).all()
    return {"data":titles}

@app.patch('/phone/{id}')
def update_phone(id: int, payload:PhoneBase ):
    note_query = session.query(PhoneModel).filter(TitleModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(TitleModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}

@app.post('/worker/add', )
def home(data: UserCreate, identity: dict):
    new_identity = identity.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_identity.update({'exp': expire})
    encoded_jwt = jwt.encode(claims=new_identity, key=SECRET_KEY, algorithm=ALGORITHM)
    hashed_password = auth_router.hash(data.password)
    c1 = WorkersModel(name=data.name,roll_id=data.roll_id,phone_id=data.phone_id,username=data.username,password=hashed_password,token=encoded_jwt)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/partner/add', )
def home(data: PartnerCreate,get_current_user : int = Depends(routers.auth_router.get_current_user)):
    c1 = PartnerModel(name=data.name,address=data.address,balance=data.balance,
                    user_id=data.user_id,phone_id=data.phone_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/taminot/add', )
def home(data: TaminotCreate, ):
    c1 = TaminotModel(name=data.name,quantity=data.quantity,price=data.price,user_id=data.user_id,partner_id=data.partner_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/store/add', )
def home(data: StoreCreate, ):
    c1 = StoreModel(name=data.name,long=data.long,lat=data.lat,user_id=data.user_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/product/add', )
def home(data: ProductCreate, ):
    c1 = ProductModel(name=data.name,quantity=data.quantity,price=data.price,
                    trade_price=data.trade_price,user_id=data.user_id,partner_id=data.partner_id,store_id=data.store_id,)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/customer/add', )
def home(data: CustomerCreate, ):
    c1 = CustomerModel(name=data.name,balance=data.balance,
                    roll_id=data.roll_id,phone_id=data.phone_id,store_id=data.store_id,)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/order/add', )
def home(data: OrderCreate, ):
    c1 = OrderModel(name=data.name,price=data.price,quantity=data.quantity,
                    customer_id=data.customer_id,phone_id=data.phone_id,store_id=data.store_id,)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/sale/add', )
def home(data: SaleCreate, ):
    c1 = SaleModel(name=data.name,price=data.price,quantity=data.quantity,
                    customer_id=data.customer_id,phone_id=data.phone_id,store_id=data.store_id,order_id = data.order_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/profit/add', )
def home(data: ProfitCreate, ):
    c1 = ProfitModel(price=data.price,comment=data.comment,
                    customer_id=data.customer_id,user_id=data.user_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@app.post('/expense/add', )
def home(data: ExpenseCreate, ):
    c1 = ExpenseModel(price=data.price,comment=data.comment,
                      type=data.type,user_id=data.user_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}



app.include_router(
    auth_router.router,
    prefix='/users',
    tags=['User Operations'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

# app.include_router(
#     title_router.router,
#     prefix='/title',
#     tags=['User Operations'],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )