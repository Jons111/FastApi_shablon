
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

router_expence = APIRouter()
@router_expence.post('/add', )
def expense(data: ExpenseCreate, ):
    c1 = ExpenseModel(price=data.price,comment=data.comment,
                      type=data.type,user_id=data.user_id)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router_expence.get('/',  status_code = 200)
def get_all_expenses(db: Session = Depends(get_db)):
    titles = db.query(ExpenseModel).all()
    return {"data":titles}

@router_expence.get('/{id}', status_code = 200)
def get_one_expense(id:int ,db: Session = Depends(get_db)):
    titles = db.query(ExpenseModel).filter(ExpenseModel.id==id).all()
    return {"data":titles}

@router_expence.patch('/{id}')
def update_expense(id: int, payload:ExpenseBase ):
    note_query = session.query(ExpenseModel).filter(ExpenseModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(ExpenseModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}
