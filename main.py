from datetime import timedelta, datetime
from typing import Optional,Union
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel
from routers import  auth_router

# database setup
from db.config import Base, engine, get_db
from models.user_model import UserModel

from db.config import Base, engine
Base.metadata.create_all(bind=engine)

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

app = FastAPI(
    title="Implementing Security",
    description="Project to implement security in FastAPI",
    version="1.0.0"
)

@app.get('/')
async def home():
    return {"message":"Welcome"}

SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# setup passlib object to manage your hashes and related policy configuration.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

"""
    Replace this list with the hash(es) you wish to support.
    this example sets pbkdf2_sha256 as the default,
    with additional support for reading legacy des_crypt hashes.

"""
# setup the security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def check_password_hash(password, hashed_passed):
    return pwd_context.verify(password, hashed_passed)

# authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    if not check_password_hash(password=password, hashed_passed=user.hashed_password):
        return False
    return user

# create access token
def create_access_token(identity: dict, expires_delta: Optional[timedelta] = None):
    """setup expiry for your tokens"""
    new_identity = identity.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # update your your dict
    new_identity.update({'exp':expire})
    # encoded token
    encoded_jwt = jwt.encode(claims=new_identity, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# get current user
async def get_identity(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # decode the token
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        identity: str = payload.get('sub')
        if identity is None:
            raise exception
    except JWTError:
        raise exception
    return identity

async def get_identity_active(identity_active: User = Depends(get_identity)):
    """
        This function is used to get the current user.
        It is used in the routers.py file.
    """
    if identity_active.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive Identity")
    return identity_active


@app.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(identity={'sub': user.id}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}


app.include_router(
    auth_router.router,
    prefix='/users',
    tags=['User Operations'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)
