
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

router_order = APIRouter()

@router_order.post('/add', )
def order(data: OrderCreate, ):
    c1 = OrderModel(name=data.name,price=data.price,quantity=data.quantity,
                    customer_id=data.customer_id,phone_id=data.phone_id,store_id=data.store_id,)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router_order.get('/',  status_code = 200)
def get_all_orders(db: Session = Depends(get_db)):
    titles = db.query(OrderModel).all()
    return {"data":titles}

@router_order.get('/{id}', status_code = 200)
def get_one_order(id:int ,db: Session = Depends(get_db)):
    titles = db.query(OrderModel).filter(OrderModel.id==id).all()
    return {"data":titles}

@router_order.patch('/{id}')
def update_order(id: int, payload:OrderBase ):
    note_query = session.query(OrderModel).filter(OrderModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(OrderModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}
