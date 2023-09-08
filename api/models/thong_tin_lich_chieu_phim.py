from pydantic import BaseModel
from typing import List

class Lich_Chieu_Item(BaseModel):
    maLichChieu: int
    maRap: str
    tenRap: str
    ngayChieuGioChieu: str
    giaVe: int
    thoiLuong: int

class Cum_Rap_Item(BaseModel):
    lichChieuPhim: List[Lich_Chieu_Item]
    maCumRap: str
    tenCumRap: str
    hinhAnh: str
    diaChi: str

class He_Thong_Rap(BaseModel):
    CumRapChieu: List[Cum_Rap_Item]
    maHeThongRap: str
    tenHeThongRap: str
    logo: str

class MovieInfo_Rap(BaseModel):
    heThongRapChieu: List[He_Thong_Rap]
    maPhim: int
    tenPhim: str
    biDanh: str
    trailer: str
    hinhAnh: str
    moTa: str
    maNhom: str
    hot: bool
    dangChieu: bool
    sapChieu: bool
    ngayKhoiChieu: str
    danhGia: float

    

