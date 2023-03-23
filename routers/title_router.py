# from typing import List
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
#
#
# #db imports
# from db.config import get_db
# from main import session
# from models.user_model import TitleModel
# from schemas.basemodels import TitleBase,TaminotCreate,TitleOut
#
# router = APIRouter()
#
# @router.get('', summary='return a list of titles', response_model=List[TitleOut], response_description='all titles', status_code = 200)
# async def get_all_tasks(db: Session = Depends(get_db)):
#     return db.query(TitleModel).all()
#
# @router.get('/{id}', response_model=TitleOut, status_code=200)
# async def get_task(id: int, db: Session = Depends(get_db)):
#     task = db.query(TitleModel).filter(TitleModel.id == id).first()
#     if task is None:
#         raise HTTPException(status_code=404, detail='task does not exist')
#     return task
#
# @router.post('/add', response_model=TitleOut, status_code=200)
# async def get_task(payload:TitleBase, db: Session):
#     title = db.query(TitleModel).filter(TitleModel.name == payload.name).first()
#     if title:
#         raise HTTPException(status_code=400, detail="Title already exists!")
#
#     else:
#         record = TitleModel(name=payload.name)
#         db.add(record)
#         db.commit()
#         db.refresh(record)
#         return record
