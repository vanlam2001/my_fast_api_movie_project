from pydantic import BaseModel
from typing import List

class LichChieuItem(BaseModel):
    maLichChieu: int
    maRap: str
    tenRap: str
    ngayKhoiChieu: str
    giaVe: int

class PhimItem(BaseModel):
    lstLichChieuTheoPhim: List[LichChieuItem]
    maPhim: int
    tenPhim: str
    hinhAnh: str
    hot: bool
    dangChieu: bool
    sapChieu: bool

class CumRapItem(BaseModel):
    danhSachPhim: List[PhimItem]
    maCumRap: str
    tenCumRap: str
    hinhAnh: str
    diaChi: str

class MovieRap(BaseModel):
    lstCumRap: List[CumRapItem]
    maHeThongRap: str
    tenHeThongRap: str
    logo: str