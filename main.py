from fastapi import FastAPI, Depends, HTTPException
from api.routes import user_management, movie_manager, he_thong_rap, quan_ly_dat_ve, lich_chieu_he_thong_rap
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# Cấu hình CORS để cho phép các yêu cầu từ tên miền React của bạn
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
        ],  # Thay bằng địa chỉ của ứng dụng React của bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(quan_ly_dat_ve.router)
app.include_router(user_management.router)
app.include_router(movie_manager.router)
app.include_router(he_thong_rap.router)
app.include_router(lich_chieu_he_thong_rap.router)







    





# https://viblo.asia/p/huong-dan-co-ban-framework-fastapi-tu-a-z-phan-2-E375zQq6lGW




