from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.thong_tin_he_thong_chieu_rap import MovieRap
from ..utils.db import get_database
from ..utils.security import get_token_authorization
from ..routes.quan_ly_dat_ve import list_lich_chieu
from ..routes.movie_manager import list_movie
from ..routes.he_thong_rap import list_cum_rap
from ..routes.he_thong_rap import list_he_thong_rap
from typing import List

router = APIRouter()

tags_rap = "Quản lý lịch chiếu hệ thống rạp"

class LichChieuItem:
    maLichChieu: int
    maRap: str
    tenRap: str
    ngayKhoiChieu: str
    giaVe: int

class PhimItem:
    lstLichChieuTheoPhim: List[LichChieuItem]
    maPhim: int
    tenPhim: str
    hinhAnh: str
    hot: bool
    dangChieu: bool
    sapChieu: bool

class CumRapItem:
    maCumRap: str
    tenCumRap: str
    hinhAnh: str
    diaChi: str
    danhSachPhim: List[PhimItem]

class HeThongRapItem:
    maHeThongRap: str
    tenHeThongRap: str
    logo: str
    lstCumRap: List[CumRapItem]

async def get_combined_data(db: AsyncIOMotorClient):
    # Lấy dữ liệu từ database 'ma_lich_chieu'
    collection_lich_chieu = db['ma_lich_chieu']
    lich_chieu_data = await collection_lich_chieu.find().to_list(length=None)

    # Lấy dữ liệu từ database 'movie'
    collection_movie = db['movie']
    movie_data = await collection_movie.find().to_list(length=None)

    # Lấy dữ liệu từ database 'thong_tin_cum_rap'
    collection_cum_rap = db['thong_tin_cum_rap']
    cum_rap_data = await collection_cum_rap.find().to_list(length=None)

    # Lấy dữ liệu từ database 'thong_tin_he_thong_rap'
    collection_he_thong_rap = db['thong_tin_he_thong_rap']
    he_thong_rap_data = await collection_he_thong_rap.find().to_list(length=None)

    # Tạo object cuối cùng
    combined_data = []

    for he_thong_rap in he_thong_rap_data:
        rap_item = HeThongRapItem()  # Khởi tạo đối tượng HeThongRapItem

        # Gán giá trị cho các thuộc tính của đối tượng
        rap_item.lstCumRap = []
        rap_item.maHeThongRap = he_thong_rap['maHeThongRap']
        rap_item.tenHeThongRap = he_thong_rap['tenHeThongRap']
        rap_item.logo = he_thong_rap.get('logo', '')
        

        for cum_rap in cum_rap_data:
            if cum_rap.get('maHeThongRap') == he_thong_rap['maHeThongRap']:
                cum_rap_item = CumRapItem()  # Khởi tạo đối tượng CumRapItem

                # Gán giá trị cho các thuộc tính của đối tượng
                cum_rap_item.maCumRap = cum_rap['maCumRap']
                cum_rap_item.tenCumRap = cum_rap['tenCumRap']
                cum_rap_item.hinhAnh = cum_rap.get('hinhAnh', '')
                cum_rap_item.diaChi = cum_rap.get('diaChi', '')
                cum_rap_item.danhSachPhim = []

                for movie in movie_data:
                    if 'maPhim' in movie and movie['maPhim'] == cum_rap.get('maPhim'):
                        lich_chieu_items = []

                        for lich_chieu in lich_chieu_data:
                            if 'maPhim' in lich_chieu and lich_chieu['maPhim'] == movie['maPhim']:
                                lich_chieu_item = LichChieuItem()  # Khởi tạo đối tượng LichChieuItem

                                # Gán giá trị cho các thuộc tính của đối tượng
                                lich_chieu_item.maLichChieu = lich_chieu['maLichChieu']
                                lich_chieu_item.maRap = lich_chieu['maRap']
                                lich_chieu_item.tenRap = lich_chieu['tenRap']
                                lich_chieu_item.ngayKhoiChieu = lich_chieu['ngayKhoiChieu']
                                lich_chieu_item.giaVe = lich_chieu['giaVe']

                                lich_chieu_items.append(lich_chieu_item)

                        phim_item = PhimItem()  # Khởi tạo đối tượng PhimItem

                        # Gán giá trị cho các thuộc tính của đối tượng
                        phim_item.lstLichChieuTheoPhim = lich_chieu_items
                        phim_item.maPhim = movie['maPhim']
                        phim_item.tenPhim = movie['tenPhim']
                        phim_item.hinhAnh = movie.get('hinhAnh', '')
                        phim_item.hot = movie.get('hot', False)
                        phim_item.dangChieu = movie.get('dangChieu', False)
                        phim_item.sapChieu = movie.get('sapChieu', False)

                        cum_rap_item.danhSachPhim.append(phim_item)

                rap_item.lstCumRap.append(cum_rap_item)

        combined_data.append(rap_item)

    return combined_data










    # API endpoint để lấy dữ liệu kết hợp từ các database
@router.get("/api/Lay-danh-sach-combined-data", tags=[tags_rap])
async def list_combined_data(token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    combined_data = await get_combined_data(db)
    return combined_data
    
    

@router.get("/api/Danh-sach-thong-tin-lich-chieu-he-thong-rap", response_model=List[MovieRap], tags=[tags_rap])
async def list_lich_chieu_rap (token: str = Depends(get_token_authorization), db: AsyncIOMotorClient = Depends(get_database)):
    collection = db['thong_tin_lich_chieu_he_thong_rap']
    lich_chieu_he_thong_rap = await collection.find().to_list(length=None)
    return lich_chieu_he_thong_rap