from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import UserModel
from schemas.basemodels import UserCreate
from passlib.context import CryptContext
pwd_context = CryptContext(schemas=['bcrypt'])

class Userservice:
    @staticmethod
    def fetch_users(db:Session):
        return db.query(UserModel).all()

    @staticmethod
    def find_user(user_id:int,db:Session):
        user = db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException
        return user

    @staticmethod
    def insert_user(payload:UserCreate,db:Session):
        user=db.query(UserModel).filter(UserModel.mail==payload.mail).first()

        if user:
            raise HTTPException(status_code=400,detail="User already exist")
        else:
            record = UserModel(username=payload.username,mail=payload.mail,password=pwd_context.hash(payload.password))
            db.add(record)
            db.commit()
            db.refresh(record)
            return record

    @staticmethod
    def delete_user(user_id:int,db:Session):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        db.delete(user)
        db.commit()
        db.refresh(user)
