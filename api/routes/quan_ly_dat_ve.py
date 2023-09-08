from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.thong_tin_ve import MovieInfoAndSeats, maLichChieu, taoLichChieu, UpdateLichChieu
from ..utils.db import get_database
from ..utils.security import get_token_authorization
from typing import List


router = APIRouter()

tags_ve = "Quản lý đặt vé"


# Quản lý danh sách vé 
@router.post("/api/Dat-ve" , tags=[tags_ve])
async def create_ve_list(ve: maLichChieu, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['danh_sach_dat_ve']
    rap_data = ve.dict()
    result = await collection.insert_one(rap_data)

    if result:
        return {"message": "Đã tạo vé thành công", "ve_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Không thể tạo rạp")




@router.post("/api/Tao-lich-chieu", tags=[tags_ve])
async def create_lich_chieu(lich_chieu: taoLichChieu, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['ma_lich_chieu']
    lich_chieu_data = lich_chieu.dict()
    result = await collection.insert_one(lich_chieu_data)

    if result:
        return {"message": "Đã tạo lịch chiếu thành công", "lich_chieu_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Không thể tạo lịch chiếu")
    

@router.get("/api/Lay-danh-sach-lich-chieu", response_model=List[taoLichChieu], tags=[tags_ve])
async def list_lich_chieu(token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['ma_lich_chieu']
    lich_chieu_data = await collection.find().to_list(length=None)
    return lich_chieu_data

@router.put("/api/Cap-nhat-lich-chieu/{malichChieu}",  tags=[tags_ve])
async def update_lich_chieu(malichChieu: int, update_lich_chieu: UpdateLichChieu, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã lịch chiếu trong database 
    collection = db['ma_lich_chieu']
    existing_lich_chieu = await collection.find_one({"maLichChieu": malichChieu})

    if existing_lich_chieu is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã lịch chiếu")
    
    update_lich_chieu_dict = update_lich_chieu.dict(exclude_unset=True)
    await collection.update_one({"maLichChieu": malichChieu}, {"$set": update_lich_chieu_dict})
    return malichChieu

@router.delete("/api/Xoa-lich-chieu/{maLichChieu}", tags=[tags_ve])
async def delete_lich_chieu(maLichChieu: int, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm lịch chiếu trong database 
    lich_chieu_data = await db.ma_lich_chieu.find_one({"maLichChieu": maLichChieu})
    if lich_chieu_data is None:
        raise HTTPException(status_code=404, detail="Lịch chiếu không tìm thấy")
    
    # Xoá lịch chiếu 
    await db.ma_lich_chieu.delete_one({"maLichChieu": maLichChieu})
    return {"message": "Lịch chiếu đã xoá thành công"}
    

@router.get("/api/Tim-thong-tin-lich-chieu", response_model=List[taoLichChieu], tags=[tags_ve])
async def find_lich_chieu(token: str = Depends(get_token_authorization) ,maLichChieu: int = Query(None, description="Mã lịch chiếu cần tìm"),db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['ma_lich_chieu']
    lich_chieu_data = await collection.find({"maLichChieu": maLichChieu}).to_list(length=None)

    query = {}
    if maLichChieu is not None:
        query['maLichChieu'] = maLichChieu
    
    lich_chieu_data = await collection.find(query).to_list(length=None)

    if not lich_chieu_data:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã lịch chiếu")
    return lich_chieu_data

    
    