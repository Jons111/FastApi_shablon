
from fastapi import APIRouter, Depends, HTTPException


from db.config import Base, engine

from sqlalchemy.orm import sessionmaker
Base.metadata.create_all(bind=engine)
#db imports
from db.config import get_db

Session = sessionmaker(bind=engine)
session = Session()

from models.user_model import *
from schemas.basemodels import *

router_taminot = APIRouter()



@router_taminot.post('/taminot/add', )
def taminot(data: TaminotCreate, ):
    c1 = TaminotModel(name=data.name,quantity=data.quantity,price=data.price,user_id=data.user_id,partner_id=data.partner_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router_taminot.get('/taminots/',  status_code = 200)
def get_all_taminot(db: Session = Depends(get_db)):
    titles = db.query(TaminotModel).all()
    return {"data":titles}

@router_taminot.get('/taminots/{id}', status_code = 200)
def get_one_taminot(id:int ,db: Session = Depends(get_db)):
    titles = db.query(TaminotModel).filter(TaminotModel.id==id).all()
    return {"data":titles}

@router_taminot.patch('/taminot/{id}')
def update_taminot(id: int, payload:TaminotBase ):
    note_query = session.query(TaminotModel).filter(TaminotModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(TaminotModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}