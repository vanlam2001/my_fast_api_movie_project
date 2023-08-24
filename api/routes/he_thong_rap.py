from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.movie import Movie_Rap, CumRapItem
from ..models.thong_tin_he_thong_chieu_rap import HeThongRapCreate
from ..utils.db import get_database
from ..utils.security import get_token_authorization
from typing import List

router = APIRouter()

tags_rap = "Quản lý rạp"

# Thông tin hệ thống rạp

@router.post("/api/Tao-thong-tin-he-thong-rap", tags=[tags_rap])
async def create_rap_list(rap: Movie_Rap, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_he_thong_rap']
    rap_data = rap.dict()
    result = await collection.insert_one(rap_data)

    if result:
        return {"message": "Đã tạo rạp thành công", "rap_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Không thể tạo rạp")
    
@router.get("/api/Lay-danh-sach-he-thong-rap", response_model=List[Movie_Rap], tags=[tags_rap])
async def list_he_thong_rap(token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_he_thong_rap']
    list_data = await collection.find().to_list(length=None)
    return list_data

@router.put("/api/Cap-nhat-thong-tin-he-thong-rap/{maHeThongRap}", tags=[tags_rap])
async def update_thong_tin_he_thong_rap(maHeThongRap: str , update_thong_tin_rap: Movie_Rap, db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã hệ thống rạp trong database
    collection = db['thong_tin_he_thong_rap']
    existing_data = await collection.find_one({"maHeThongRap": maHeThongRap})

    if existing_data is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã hệ thống thông tin rạp")
    
    # Cập nhật thông tin rạp
    update_rap_dict = update_thong_tin_rap.dict(exclude_unset=True)
    await collection.update_one({"maHeThongRap": maHeThongRap}, {"$set": update_rap_dict})
    return update_thong_tin_rap

@router.delete("/api/Xoa-thong-tin-he-thong-rap/{maHeThongRap}", tags=[tags_rap])
async def delete_thong_tin_rap(maHeThongRap: str = Query(..., description="Mã hệ thống rạp cần xoá"),token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã hệ thống rạp trong database
    collection = db['thong_tin_he_thong_rap']

    list_data = await collection.find_one({"maHeThongRap": maHeThongRap})
    if list_data is None:
        raise HTTPException(status_code=404, detail="Mã hệ thống rạp không tìm thấy")
    # xoá mã rạp
    await collection.delete_one({"maHeThongRap": maHeThongRap})
    return {"message": "Đã xoá thông tin rạp thành công"}

# Cụm rạp

@router.post("/api/Tao-thong-tin-cum-rap", tags=[tags_rap])
async def create_cup_rap(rap: CumRapItem, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_cum_rap']
    cum_rap_data = rap.dict()
    result = await collection.insert_one(cum_rap_data)

    if result:
        return {"message": "Đã tạo cụm rạp thành công", "rap_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Không thể tạo cụm rạp")

@router.get("/api/Lay-danh-sach-cum-rap", response_model=List[CumRapItem], tags=[tags_rap])
async def list_cum_rap(token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_cum_rap']
    list_data = await collection.find().to_list(length=None)
    return list_data

@router.put("/api/Cap-nhat-thong-tin-cum-rap/{maHeThongRap}", tags=[tags_rap])
async def update_thong_tin_cum_rap(maHeThongRap: str, update_thong_tin_cum_rap: CumRapItem, db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã hệ thống rạp trong database 
    collection = db['thong_tin_cum_rap']
    existing_data = await collection.find_one({"maHeThongRap": maHeThongRap})

    if existing_data is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã hệ thống thông tin cụm rạp")
    
    # Cập nhật thông tin cụm rạp
    update_cum_rap_dict = update_thong_tin_cum_rap.dict(exclude_unset=True)
    await collection.update_one({"maHeThongRap": maHeThongRap}, {"$set": update_cum_rap_dict})
    return update_thong_tin_cum_rap

@router.delete("/api/Xoa-thong-tin-cum-rap/{maHeThongRap}", tags=[tags_rap])
async def delete_thong_tin_cum_rap(maHeThongRap: str = Query(..., description="Mã hệ thống cụm rạp cần xóa"), db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã hệ thống rạp trong database
    collection = db['thong_tin_cum_rap']

    list_data = await collection.find_one({"maHeThongRap": maHeThongRap})
    if list_data is None:
        raise HTTPException(status_code=404, detail="Mã hệ thống cụm rạp không tìm thấy")
    # xóa mã cụp rạp
    await collection.delete_one({"maHeThongRap": maHeThongRap})
    return {"message": "Đã xóa thông tin cụm rạp thành công"}

@router.post("/api/Tao-thong-tin-lich-chieu-he-thong-rap", tags=[tags_rap])
async def create_thong_tin_lich_chieu(rap: HeThongRapCreate, db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_lich_chieu_he_thong_rap']
    lich_chieu_data = rap.dict()
    result = await collection.insert_one(lich_chieu_data)

    if result:
        return {"message": "Đã tạo lịch chiếu thành công", "rap_id": str(result.inserted_id)}
    else:
        raise HeThongRapCreate(status_code=500, detail="Không thể tạo lịch chiếu")
    

    