from pydantic import BaseModel
from typing import List

class Movie_Info(BaseModel):
    maPhim: int
    tenPhim: str
    biDanh: str
    trailer: str
    hinhAnh: str
    moTa: str
    ngayKhoiChieu: str
    danhGia: int
    hot: bool
    dangChieu: bool
    sapChieu: bool

class Movie_Banner(BaseModel):
    maBanner: int
    banner: str

class Movie_Rap(BaseModel):
    maHeThongRap: str
    tenHeThongRap: str
    biDanh: str
    logo: str

class RapItem(BaseModel):
    maRap: int
    tenRap: str

class CumRapItem(BaseModel):
    maHeThongRap: str
    maCumRap: str
    tenCumRap: str
    diaChia: str
    danhSachRap: List[RapItem]