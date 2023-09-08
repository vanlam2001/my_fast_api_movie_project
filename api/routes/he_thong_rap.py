from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.movie import Movie_Rap, CumRapItem, Update_Movie_Rap, Update_Cum_Rap_Item

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
    
@router.get("/api/Tim-thong-tin-he-thong-rap", response_model=List[Movie_Rap], tags=[tags_rap])
async def list_he_thong_rap(token: str = Depends(get_token_authorization) ,maHeThongRap: str = Query(None, description="Tìm mã hệ thống rạp"),db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_he_thong_rap']
    list_data = await collection.find({"maHeThongRap": maHeThongRap}).to_list(length=None)
    
    query = {}

    if maHeThongRap is not None:
        query['maHeThongRap'] = {"$regex": f".*{maHeThongRap}.*", "$options": "i"}
    list_data = await collection.find(query).to_list(length=None)

    if not list_data:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã hệ thống rạp")
    return list_data

@router.get("/api/Lay-danh-thong-tin-he-thong-rap" , response_model=List[Movie_Rap], tags=[tags_rap])
async def list_he_thong_rap(token: str = Depends(get_token_authorization) , db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_he_thong_rap']
    movie_data = await collection.find().to_list(length=None)
    return movie_data


@router.put("/api/Cap-nhat-thong-tin-he-thong-rap/{maHeThongRap}", tags=[tags_rap])
async def update_thong_tin_he_thong_rap(maHeThongRap: str , update_thong_tin_rap: Update_Movie_Rap, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
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

# ... (code định nghĩa các BaseModel và endpoint khác ở đây) ...

@router.post("/api/Tao-thong-tin-cum-rap", tags=[tags_rap])
async def create_cup_rap(rap: CumRapItem, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    # Truy vấn maHeThongRap từ thong_tin_he_thong_rap dựa trên thông tin cụm rạp
    system_collection = db['thong_tin_he_thong_rap']
    system_info = await system_collection.find_one({"maHeThongRap": rap.maHeThongRap})

    if not system_info:
        raise HTTPException(status_code=404, detail="Không tìm thấy hệ thống rạp trong database")

    # Kiểm tra xem `maRap` có tồn tại trong danh sách danhSachRap của đối tượng rap không
    lich_chieu_collection = db['ma_lich_chieu']
    existing_lich_chieu = await lich_chieu_collection.find_one({"maRap": rap.danhSachRap[0].maRap})

    if not existing_lich_chieu:
        raise HTTPException(status_code=400, detail="maRap không tồn tại trong database ma_lich_chieu")

    # Tạo thông tin cụp rạp mới dựa trên thông tin từ đối tượng rap và maHeThongRap từ trong thong_tin_he_thong_rap
    cum_rap_data = rap.dict()
    cum_rap_data["maHeThongRap"] = system_info["maHeThongRap"]

    # Thêm thông tin cụp rạp vào databases
    collection = db['thong_tin_cum_rap']
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

@router.get("/api/Tim-thong-tin-cum-rap", response_model=List[CumRapItem], tags=[tags_rap])
async def tim_thong_tin_cum_rap(token: str = Depends(get_token_authorization), maHeThongRap: str = Query(None ,description="Tìm mã hệ thống rạp"), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_cum_rap']
    list_data = await collection.find({"maHeThongRap": maHeThongRap}).to_list(length=None)

    query = {}

    if maHeThongRap is not None:
        query['maHeThongRap'] = {"$regex": f".*{maHeThongRap}.*", "$options": "i"}
    list_data = await collection.find(query).to_list(length=None)

    if not list_data:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã hệ thống rạp")
    return list_data



@router.put("/api/Cap-nhat-thong-tin-cum-rap/{maHeThongRap}", tags=[tags_rap])
async def update_thong_tin_cum_rap(maHeThongRap: str, update_thong_tin_cum_rap: Update_Cum_Rap_Item,token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
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




# Lịch chiếu 
# @router.post("/api/Tao-thong-tin-lich-chieu-he-thong-rap", tags=[tags_rap])
# async def create_thong_tin_lich_chieu(rap: HeThongRapCreate, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
#     collection = db['thong_tin_lich_chieu_he_thong_rap']
#     lich_chieu_data = rap.dict()
#     result = await collection.insert_one(lich_chieu_data)

#     if result:
#         return {"message": "Đã tạo lịch chiếu thành công", "rap_id": str(result.inserted_id)}
#     else:
#         raise HeThongRapCreate(status_code=500, detail="Không thể tạo lịch chiếu")
    

    
# @router.get("/api/Lay-thong-tin-lich-chieu-he-thong-rap", response_model=List[HeThongRapCreate] ,tags=[tags_rap])
# async def list_thong_tin_lich_chieu(token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
#     collection = db['thong_tin_lich_chieu_he_thong_rap']
#     list_data = await collection.find().to_list(length=None)
#     return list_data
    
# @router.put("/api/Cap-nhat-thong-tin-lich-chieu-he-thong-rap", tags=[tags_rap])
# async def update_thong_tin_lich_chieu(maHeThongRap: str, update_thong_tin_lich_chieu: HeThongRapCreate, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
#     # Tìm mã hệ thống trong databases 
#     collection = db['thong_tin_lich_chieu_he_thong_rap']
#     existing_data = await collection.find_one({"maHeThongRap": maHeThongRap})

#     if existing_data is None:
#         raise HTTPException(status_code=404, detail="Không tìm thấy mã hệ thống thông tin lịch chiếu")
#     # Cập nhật thông tin lịch chiếu
#     update_lich_chieu_dict = update_thong_tin_lich_chieu.dict(exclude_unset=True)
#     await collection.update_one({"maHeThongRap": maHeThongRap}, {"$set": update_lich_chieu_dict})
#     return update_thong_tin_lich_chieu

# @router.delete("/api/Xoa-thong-tin-lich-chieu-he-thong-rap/{maHeThongRap}", tags=[tags_rap])
# async def delete_lich_chieu_he_thong(maHeThongRap: str = Query(..., description="Mã hệ thống lịch chiếu cần xoá"), token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
#     # Tìm mã hệ thống lịch chiếu trong databases 
#     collection = db['thong_tin_lich_chieu_he_thong_rap']

#     list_data = await collection.find_one({"maHeThongRap": maHeThongRap})
#     if list_data is None:
#         raise HTTPException(status_code=404, detail="Không tìm thấy mã hệ thống thông tin lịch chiếu")
    
#     # xoá lịch chiếu
#     await collection.delete_one({"maHeThongRap": maHeThongRap})
#     return {"message": "Đã xoá thông tin lịch chiếu thành công"}

