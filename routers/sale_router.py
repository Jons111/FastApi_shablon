
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

router_sale = APIRouter()


@router_sale.post('/sale/add', )
def sale(data: SaleCreate, ):
	# For sale add
	c1 = SaleModel(name=data.name ,price=data.price ,quantity=data.quantity,
	               customer_id=data.customer_id ,phone_id=data.phone_id ,store_id=data.store_id ,order_id = data.order_id)
	session.add(c1)
	session.commit()
	# For Taminot update
	product_from_taminot = session.query(TaminotModel).filter(TaminotModel.name == data.name)
	db_note = product_from_taminot.first()
	quantity = db_note.quantity -data.quantity
	user_id  = db_note.user_id
	update_data = {"quantity" :quantity}
	product_from_taminot.filter(TaminotModel.name == data.name).update(update_data, synchronize_session=False)
	# For profit add
	product_from_products = session.query(ProductModel).filter(ProductModel.name == data.name).first()
	
	product_price = product_from_products.price
	profit_from_product = (data.price - product_price ) *data.quantity
	profit_ = ProfitModel(price=profit_from_product, comment="From customer",
	                      customer_id=data.customer_id, user_id=user_id)
	session.add(profit_)
	session.commit()
	
	
	return {"data": data.dict()}

@router_sale.get('/sale/',  status_code = 200)
def get_all_sales(db: Session = Depends(get_db)):
	titles = db.query(SaleModel).all()
	return {"data" :titles}

@router_sale.get('/sale/{id}', status_code = 200)
def get_one_sale(id :int ,db: Session = Depends(get_db)):
	titles = db.query(SaleModel).filter(SaleModel.id == id).all()
	return {"data": titles}


@router_sale.patch('/sale/{id}')
def update_sale(id: int, payload: SaleBase):
	note_query = session.query(SaleModel).filter(SaleModel.id == id)
	db_note = note_query.first()
	update_data = payload.dict()
	note_query.filter(SaleModel.id == id).update(update_data, synchronize_session=False)
	session.commit()
	session.refresh(db_note)
	return {"status": "success", "note": db_note}
