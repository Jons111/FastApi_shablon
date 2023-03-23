from typing import List
from fastapi import APIRouter, Depends, HTTPException

from db.config import Base, engine

from sqlalchemy.orm import sessionmaker
Base.metadata.create_all(bind=engine)
#db imports
from db.config import get_db

Session = sessionmaker(bind=engine)
session = Session()

from models.user_model import TitleModel
from schemas.basemodels import TitleBase,TaminotCreate,TitleOut

router = APIRouter()


@router.post('/add', status_code=201)
def title(data: TitleBase, ):
    c1 = TitleModel(name=data.name)
    session.add(c1)
    session.commit()
    return {"data": data.dict()}

@router.get('/',  status_code = 200 )
def get_all_titles(db: Session = Depends(get_db)):
    titles = db.query(TitleModel).all()
    return {"data":titles}

@router.get('{id}', status_code = 200)
def get_one_title(id:int ,db: Session = Depends(get_db)):
    titles = db.query(TitleModel).filter(TitleModel.id==id).all()
    return {"data":titles}

@router.patch('{id}')
def update_title(id: int, payload:TitleBase ):
    note_query = session.query(TitleModel).filter(TitleModel.id == id)
    db_note = note_query.first()
    update_data = payload.dict()
    note_query.filter(TitleModel.id == id).update(update_data,  synchronize_session=False)
    session.commit()
    session.refresh(db_note)
    return {"status": "success", "note": db_note}
