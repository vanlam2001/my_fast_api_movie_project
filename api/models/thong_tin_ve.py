from pydantic import BaseModel
from typing import List

# Data models 
class Ghe(BaseModel):
    maGhe: int
    tenGhe: str
    maRap: int
    loaiGhe: str
    stt: str
    giaVe: int
    daDat: bool
    taiKhoanNguoiDat: str = None

class ThongTinPhim(BaseModel):
    maLichChieu: int
    tenCumRap: str
    tenRap: str
    diaChi: str
    tenPhim: str
    hinhAnh: str
    ngayChieu: str
    gioChieu: str

class MovieInfoAndSeats(BaseModel):
    thongTinPhim: ThongTinPhim
    danhSachGhe: List[Ghe]

class danhSachVe(BaseModel):
    maGhe: int
    giaVe: int

class maLichChieu(BaseModel):
    maLichChieu: int
    danhSachVe: List[danhSachVe]


class taoLichChieu(BaseModel):
    maPhim: int
    maLichChieu: int
    ngayChieuGioChieu: str
    maRap: int
    giaVe: int
    thoiluong: str

class UpdateLichChieu(BaseModel):
    maPhim: int
    ngayChieuGioChieu: str
    maRap: int
    giaVe: int
    thoiluong: str


