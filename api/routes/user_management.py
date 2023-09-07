from fastapi import APIRouter, Depends, HTTPException, Header
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.register import UserInfo, UserType, User_Info_Type, Update_User
from ..models.login import UserLogin
from ..models.register import get_password_hash, verify_password
from ..utils.db import get_database
from ..utils.security import get_token_authorization
from typing import List





router = APIRouter()



tags_user = "Quản lý người dùng"
tags_auth = "Đăng nhập & Đăng ký"

@router.post("/api/Dang-ky", tags=[tags_auth])
async def register(user: UserInfo, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    user_data = user.dict()

    # Kiểm tra xem tài khoản đã tồn tại chưa 
    existing_user = await db.users.find_one({"username": user_data["username"]})
    if existing_user:
        return {"message": "Tài khoản đã tồn tại"}
    
    # Kiểm tra xem email đã tồn tại chưa 
    existing_email = await db.users.find_one({"email": user_data["email"]})
    if existing_email:
        return {"message": "Email đã tồn tại"}
    # Kiểm tra xem phone_number đã tồn tại chưa 
    existing_phone_number = await db.users.find_one({"phone_number": user_data["phone_number"]})
    if existing_phone_number:
        return {"message": "Số điện thoại đã tồn tại"}
    
    # Kiểm tra mật khẩu trùng khớp 
    if user_data["password"] != user_data["confirm_password"]:
        return {"message": "Mật khẩu không khớp nhau"}

    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    hashed_password = get_password_hash(user_data["password"])
    user_data["password"] = hashed_password
    del user_data["confirm_password"]

    # Lấy thông tin loại người dùng từ cơ sở dữ liệu
    user_type = await db.loaiNguoiDung.find_one({"maLoaiNguoiDung": user_data["maLoaiNguoiDung"]})
    if user_type:
        user_data["tenLoai"] = user_type["tenLoai"]

        # Lưu thông tin người dùng vào MongoDB
        await db.users.insert_one(user_data)
        return {"message": "Đăng ký thành công"}
    else:
        return {"message": "Loại người dùng không hợp lệ"}

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
    
    # Xác thực thành công, trả về thông tin tài khoản
    user_info = {
        "username": user_data["username"],
        "password": user_data["password"],
        "phone_number": user_data["phone_number"],
        "email": user_data["email"],
        "full_name": user_data["full_name"],
        "maLoaiNguoiDung": user_data["maLoaiNguoiDung"],
        "tenLoai": user_data["tenLoai"],
        "message": "Đăng nhập thành công"
    }

    return user_info

@router.get("/api/Danh-sach-nguoi-dung", response_model=List[User_Info_Type], tags=[tags_user])
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


@router.get("/api/kiem-tra-ten-nguoi-dung/{username}", tags=[tags_user])
async def check_username_exists(username: str, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    user = await db.users.find_one({"username": username}, {"id": 0})
    if user:
        return {"exists": True}
    else:
        return {"exists": False}



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
async def update_user(username: str, update_user: Update_User, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
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


# @router.post("/api/Them-nguoi-dung", tags=[tags_user])
# async def add_user(user: User_Info_Type,token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
#     user_data = user.dict()
#     # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
#     hashed_password = get_password_hash(user_data["password"])
#     user_data["password"] = hashed_password

#     # Lưu thông tin người dùng vào MongoDB
#     await db.users.insert_one(user_data)
#     return {"message": "Thêm người dùng thành công"}

