
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

router_customer = APIRouter()
@router_customer.post('/add', )
def customer(data: CustomerCreate, ):
    c1 = CustomerModel(name=data.name,balance=data.balance,
                    roll_id=data.roll_id,phone_id=data.phone_id,store_id=data.store_id,)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router_customer.get('/',  status_code = 200)
def get_all_customers(db: Session = Depends(get_db)):
    titles = db.query(CustomerModel).all()
    return {"data":titles}

@router_customer.get('/{id}', status_code = 200)
def get_one_customer(id:int ,db: Session = Depends(get_db)):
    titles = db.query(CustomerModel).filter(CustomerModel.id==id).all()
    return {"data":titles}

@router_customer.patch('/{id}')
def update_customer(id: int, payload:CustomerBase ):
    note_query = session.query(CustomerModel).filter(CustomerModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(CustomerModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}