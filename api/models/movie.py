from pydantic import BaseModel, validator
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
    tenBanner: str
    banner: str

class Banner(BaseModel):
    tenBanner: str
    banner: str    

class Movie_Rap(BaseModel):
    maHeThongRap: str
    tenHeThongRap: str
    biDanh: str
    logo: str

class Update_Movie_Rap(BaseModel):
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

class Update_Cum_Rap_Item(BaseModel):
    maCumRap: str
    tenCumRap: str
    diaChia: str
    danhSachRap: List[RapItem]

    
