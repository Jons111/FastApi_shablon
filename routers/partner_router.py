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

router_partner = APIRouter()

@router_partner.post('/add', )
def partner(data: PartnerCreate,): #get_current_user : int = Depends(routers.auth_router.get_current_user)
    c1 = PartnerModel(name=data.name,address=data.address,balance=data.balance,
                    user_id=data.user_id,phone_id=data.phone_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router_partner.get('/',  status_code = 200)
def get_all_partners(db: Session = Depends(get_db)):
    titles = db.query(PartnerModel).all()
    return {"data":titles}

@router_partner.get('{id}', status_code = 200)
def get_one_partner(id:int ,db: Session = Depends(get_db)):
    titles = db.query(PartnerModel).filter(PartnerModel.id==id).all()
    return {"data":titles}

@router_partner.patch('{id}')
def update_partner(id: int, payload:PartnerBase ):
    note_query = session.query(PartnerModel).filter(PartnerModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(PartnerModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}