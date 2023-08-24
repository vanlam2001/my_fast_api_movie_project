from fastapi import APIRouter, Depends, HTTPException, Header
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.register import UserInfo, UserType, User_Info_Type
from ..models.login import UserLogin
from ..models.register import get_password_hash, verify_password
from ..utils.db import get_database
from ..utils.security import get_token_authorization
from typing import List




router = APIRouter()



tags_user = "Quản lý người dùng"
tags_auth = "Đăng nhập & Đăng ký"

@router.post("/api/Dang-ky", tags=[tags_auth])
async def register(user: UserInfo, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    user_data = user.dict()
    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu 
    hashed_password = get_password_hash(user_data["password"])
    user_data["password"] = hashed_password


    # Lưu thông tin người dùng vào MongoDB
    await db.users.insert_one(user_data)
    return {"message": "Đăng ký thành công"}

@router.post("/api/Dang-nhap", tags=[tags_auth])
async def login(user_login: UserLogin,token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    username = user_login.username
    password = user_login.passwords 
    

    # Tìm người dùng trong databases 
    user_data = await db.users.find_one({"username": username})
    if user_data is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài nguyên")
    hashed_password = user_data["password"]
    

    # Xác thực mật khẩu 
    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=404, detail="Không tìm thấy tài nguyên")
    return {"message": "Đăng nhập thành công"}

@router.get("/api/Danh-sach", response_model=List[User_Info_Type], tags=[tags_user])
async def get_user_list(token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    users = await db.users.find({}, {"id": 0}).to_list(length=None)
    user_list = []
    for user in users:
        user_info = User_Info_Type(
            username=user.get("username", ""),
            password=user.get("password", ""),
            phone_number=user.get("phone_number", ""),
            email=user.get("email", ""),
            full_name=user.get("full_name", ""),
            maLoaiNguoiDung=user.get("maLoaiNguoiDung", ""),
            tenLoai=user.get("tenLoai", "")
        )
        user_list.append(user_info)
    return user_list




@router.delete("/api/Xoa-tai-khoan/{username}", tags=[tags_user])
async def delete_user(username: str, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm người dùng trong cơ sở dữ liệu
    user_data = await db.users.find_one({"username": username})
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Xoá người dùng
    await db.users.delete_one({"username": username})
    return {"message": "User deleted successfully"}


@router.get("/api/Tim-kiem", response_model=List[User_Info_Type], tags=[tags_user])
async def search_users(query: str ,token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm kiếm các người dùng với thông tin chứa query trong username hoặc email 
    users = await db.users.find(
       {"$or": [{"username": {"$regex": query, "$options": "i"}},
                 {"email": {"$regex": query, "$options": "i"}}]},
        {"id": 0}
    ).to_list(length=None)

    user_list = []
    for user in users:
        user_info = User_Info_Type(
            username=user.get("username", ""),
            password=user.get("password", ""),
            phone_number=user.get("phone_number", ""),
            email=user.get("email", ""),
            full_name=user.get("full_name", ""),
            maLoaiNguoiDung=user.get("maLoaiNguoiDung", ""),
            tenLoai=user.get("tenLoai", "")
        )
        user_list.append(user_info)

        return user_list

@router.put("/api/Chinh-sua-thong-tin/{username}", tags=[tags_user])
async def update_user(username: str, update_user: User_Info_Type, db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm người dùng trong databases 
    existing_user = await db.users.find_one({"username": username})

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Cập nhật thông tin người dùng
    updated_data = update_user.dict(exclude_unset=True)
    if "password" in updated_data:
        # Nếu có thay đổi mật khẩu, mã hoá mật khẩu mới trước khi cập nhật
        updated_data["password"] = get_password_hash(updated_data["password"])
    await db.users.update_one({"username": username}, {"$set": updated_data})
    return {"message": "User information updated successfully"}



@router.get("/api/Loai-nguoi-dung", response_model=List[UserType], tags=[tags_user])
async def get_user_types_endpoint(database: AsyncIOMotorClient = Depends(get_database)):
    user_types_collection = database["loaiNguoiDung"]
    user_types = []
    async for user_type in user_types_collection.find():
        user_types.append(UserType(**user_type))
    return user_types


@router.post("/api/Them-nguoi-dung", tags=[tags_user])
async def add_user(user: User_Info_Type, db: AsyncIOMotorClient = Depends(get_database)):
    user_data = user.dict()
    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    hashed_password = get_password_hash(user_data["password"])
    user_data["password"] = hashed_password

    # Lưu thông tin người dùng vào MongoDB
    await db.users.insert_one(user_data)
    return {"message": "Thêm người dùng thành công"}

