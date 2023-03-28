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

router_worker = APIRouter()






@router_worker.post('/worker/add', )
def worker(data: UserCreate, identity: dict):
    new_identity = identity.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_identity.update({'exp': expire})
    encoded_jwt = jwt.encode(claims=new_identity, key=SECRET_KEY, algorithm=ALGORITHM)
    hashed_password = auth_router.hash(data.password)
    c1 = WorkersModel(name=data.name,roll_id=data.roll_id,phone_id=data.phone_id,username=data.username,password=hashed_password,token=encoded_jwt)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router_worker.get('/workers/',  status_code = 200)
def get_all_workers(db: Session = Depends(get_db)):
    titles = db.query(WorkersModel).all()
    return {"data":titles}

@router_worker.get('/worker/{id}', status_code = 200)
def get_one_worker(id:int ,db: Session = Depends(get_db)):
    titles = db.query(WorkersModel).filter(WorkersModel.id==id).all()
    return {"data":titles}

@router_worker.patch('/worker/{id}')
def update_worker(id: int, payload:UserBase ):
    note_query = session.query(WorkersModel).filter(WorkersModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(WorkersModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}

