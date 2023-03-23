
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

router_store = APIRouter()

@router_store.post('/store/add', )
def store(data: StoreCreate, ):
    c1 = StoreModel(name=data.name,long=data.long,lat=data.lat,user_id=data.user_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}
@router_store.get('/stores/',  status_code = 200)
def get_all_stores(db: Session = Depends(get_db)):
    titles = db.query(StoreModel).all()
    return {"data":titles}

@router_store.get('/store/{id}', status_code = 200)
def get_one_store(id:int ,db: Session = Depends(get_db)):
    titles = db.query(StoreModel).filter(StoreModel.id==id).all()
    return {"data":titles}

@router_store.patch('/store/{id}')
def update_store(id: int, payload:StoreBase ):
    note_query = session.query(StoreModel).filter(StoreModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(StoreModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}