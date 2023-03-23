from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.config import Base, engine, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import sessionmaker

from routers import auth_router

Base.metadata.create_all(bind=engine)
#db imports
from db.config import get_db

Session = sessionmaker(bind=engine)
session = Session()

from models.user_model import *
from schemas.basemodels import *

router_phone = APIRouter()


@router_phone.post('/add', )
def home(data: PhoneCreate, ):
    c1 = PhoneModel(type_id=data.type_id,number=data.number,name=data.name)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}
@router_phone.get('/',  status_code = 200)
def get_all_phones(db: Session = Depends(get_db)):
    titles = db.query(PhoneModel).all()
    return {"data":titles}

@router_phone.get('/{id}', status_code = 200)
def get_one_phone(id:int ,db: Session = Depends(get_db)):
    titles = db.query(PhoneModel).filter(PhoneModel.id==id).all()
    return {"data":titles}

@router_phone.patch('/{id}')
def update_phone(id: int, payload:PhoneBase ):
    note_query = session.query(PhoneModel).filter(TitleModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(TitleModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}