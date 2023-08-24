from pydantic import BaseModel
from typing import List

class LichChieuTheoPhimBase(BaseModel):
    maLichChieu: int
    maRap: str
    tenRap: str
    ngayKhoiChieu: str
    giaVe: int

class PhimBase(BaseModel):
    lstLichChieuTheoPhim: List[LichChieuTheoPhimBase]
    maPhim: int
    tenPhim: str
    hinhAnh: str
    hot: bool
    dangChieu: bool
    sapChieu: bool

class CumRapBase(BaseModel):
    danhSachPhim: List[PhimBase]
    maCumRap: str
    tenCumRap: str
    hinhAnh: str
    diaChi: str

class HeThongRapBase(BaseModel):
    lstCumRap: List[CumRapBase]
    maHeThongRap: str
    tenHeThongRap: str
    logo: str

class HeThongRapCreate(HeThongRapBase):
    pass