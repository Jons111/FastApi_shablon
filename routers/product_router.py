
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

router_product = APIRouter()
@router_product.post('/product/add', )
def product(data: ProductCreate, ):
    c1 = ProductModel(name=data.name,quantity=data.quantity,price=data.price,
                    trade_price=data.trade_price,user_id=data.user_id,partner_id=data.partner_id,store_id=data.store_id,)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}
@router_product.get('/product/',  status_code = 200)
def get_all_products(db: Session = Depends(get_db)):
    titles = db.query(ProductModel).all()
    return {"data":titles}

@router_product.get('/product/{id}', status_code = 200)
def get_one_product(id:int ,db: Session = Depends(get_db)):
    titles = db.query(ProductModel).filter(ProductModel.id==id).all()
    return {"data":titles}

@router_product.patch('/product/{id}')
def update_product(id: int, payload:ProductBase ):
    note_query = session.query(ProductModel).filter(ProductModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(ProductModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}