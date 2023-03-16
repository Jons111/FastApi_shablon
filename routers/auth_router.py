from passlib.context import CryptContext

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel



router=APIRouter()

# setups for JWT
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context=CryptContext(schemes=['bcrypt'])

#setup the security
OAuth2_schema=OAuth2PasswordBearer(tokenUrl='token')

# token
class Token(BaseModel):
    access_token: str
    token_type: str



































