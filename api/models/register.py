from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext


class UserInfo(BaseModel):
    username: str
    password: str
    phone_number: str
    email: str
    full_name: str

class UserType(BaseModel):
    maLoaiNguoiDung: str
    tenLoai: str

class User_Info_Type(BaseModel):
    username: str
    password: str
    phone_number: str
    email: str
    full_name: str
    maLoaiNguoiDung: Optional[str]
    tenLoai: Optional[str]



class HashedPassword:
    def __init__(self, hashed_password: str):
        self.hashed_password = hashed_password

class UserInDB(UserInfo, HashedPassword):
    pass 

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)
