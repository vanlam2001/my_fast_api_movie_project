from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.movie import Movie_Info, Movie_Banner, Banner
from ..utils.db import get_database
from ..utils.security import get_token_authorization
from typing import List


router = APIRouter()

tags_movie = "Quản Lý phim"

@router.post("/api/Tao-danh-sach-phim", tags=[tags_movie])
async def create_movie_list(movie: Movie_Info, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Truy vấn mã phim từ database lịch chiếu 
    system_collection = db['ma_lich_chieu']
    system_info = await system_collection.find_one({"maPhim": movie.maPhim})

    if not system_info:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã phim")
    
    # Tạo thông tin phim mới dựa trên mã phim của lịch chiếu 
    movie_data = movie.dict()
    movie_data["maPhim"] = system_info["maPhim"]
    
    # Thêm thông tin phim và database movie 
    collection = db['movie']
    result = await collection.insert_one(movie_data)

    if result:
        return {"message": "Đã tạo phim thành công", "movie_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Không thể tạo phim")


@router.get("/api/Lay-danh-sach-phim", response_model=List[Movie_Info], tags=[tags_movie])
async def list_movie(token: str = Depends(get_token_authorization) , db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['movie']
    movie_data = await collection.find().to_list(length=None)
    return movie_data

@router.get("/api/Lay-thong-tin-phim", response_model=List[Movie_Info], tags=[tags_movie])
async def find_movie_by_id(token: str = Depends(get_token_authorization) ,maPhim: int = Query(None, description="Mã phim cần tìm"),tenPhim: str = Query(None, description="Tên phim cần tìm") ,db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['movie']
    movie_data = await collection.find({"maPhim": maPhim}).to_list(length=None)

    query = {}

    if maPhim is not None:
        query['maPhim'] = maPhim
    if tenPhim is not None:
        query['tenPhim'] = {"$regex": f".*{tenPhim}.*", "$options": "i"}
    
    movie_data = await collection.find(query).to_list(length=None)

    if not movie_data:
        raise HTTPException(status_code=404, detail="Không tìm phim theo yêu cầu")
    
    return movie_data




@router.delete("/api/Xoa-phim/{maPhim}", tags=[tags_movie])
async def delete_movie(maPhim: int = Query(..., description="Mã phim cần xoá"), token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã phim trong databases
    movie_data = await db.movie.find_one({"maPhim": maPhim})
    if movie_data is None:
        raise HTTPException(status_code=404, detail="Mã phim không tìm thấy")
    # xoá phim
    await db.movie.delete_one({"maPhim": maPhim})
    return {"message": "Phim đã xoá thành công"}


@router.put("/api/cap-nhat-thong-tin-phim/{maPhim}", tags=[tags_movie])
async def update_movie(maPhim: int, update_movie: Movie_Info, token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã phim trong databases 
    collection = db['movie']
    existing_movie = await collection.find_one({"maPhim": maPhim})

    if existing_movie is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã phim")
    
    updated_movie_dict = update_movie.dict(exclude_unset=True)
    await collection.update_one({"maPhim": maPhim}, {"$set": updated_movie_dict})
    return update_movie
    
@router.post("/api/Tao-banner", tags=[tags_movie])
async def create_banner_movie_list(movie: Movie_Banner, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['banner']
    movie_data = movie.dict()
    result = await collection.insert_one(movie_data)

    if result:
        return {"message" : "Đã tạo thành công banner", "movie_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Không thể tạo Banner")

@router.get("/api/Lay-danh-sach-banner", response_model=List[Movie_Banner], tags=[tags_movie])
async def list_banner(token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['banner']
    banner_data = await collection.find().to_list(length=None)
    return banner_data

@router.delete("/api/Xoa-banner/{maBanner}", tags=[tags_movie])
async def delete_banner(maBanner: int = Query(..., description="Mã banner cần xóa"), token: str = Depends(get_token_authorization) ,db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm banner trong database 
    collection = db['banner']
    banner_data = await collection.find_one({"maBanner": maBanner})
    if banner_data is None:
        raise HTTPException(status_code=404, detail="Banner không tìm thấy")
    # xóa banner 
    await collection.delete_one({"maBanner": maBanner})
    return {"message": "Banner đã xóa thành công"}

@router.put("/api/Cap-nhat-Banner/{maBanner}", tags=[tags_movie])
async def update_banner(maBanner: int, update_banner: Banner, token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    # Tìm mã banner trong databases 
    collection = db['banner']
    existing_banner = await collection.find_one({"maBanner": maBanner})

    if existing_banner is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã banner")
    
    updated_banner_dict = update_banner.dict(exclude_unset=True)
    await collection.update_one({"maBanner": maBanner}, {"$set": updated_banner_dict})
    return update_banner
    
@router.get("/api/Tim-thong-tin-banner", response_model=List[Movie_Banner], tags=[tags_movie])
async def find_banner_by_id(token: str = Depends(get_token_authorization) ,maBanner: int = Query(None, description="Mã banner cần tìm"),tenBanner: str = Query(None, description="Tên banner cần tìm") ,db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['banner']
    banner_data = await collection.find({"maBanner": maBanner}).to_list(length=None)

    query = {}

    if maBanner is not None:
        query['maBanner'] = maBanner
    if tenBanner is not None:
        query['tenBanner'] = {"$regex": f".*{tenBanner}.*", "$options": "i"}
    
    banner_data = await collection.find(query).to_list(length=None)

    if not banner_data:
        raise HTTPException(status_code=404, detail="Không tìm phim theo yêu cầu")
    
    return banner_data

    
    
    






