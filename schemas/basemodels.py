from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    mail: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
