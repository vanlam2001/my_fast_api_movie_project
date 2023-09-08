from pydantic import BaseModel

class Lich_Chieu(BaseModel):
    maPhim: int
    maLichChieu: int
    ngayChieuGioChieu: str
    maRap: str
    giaVe: int