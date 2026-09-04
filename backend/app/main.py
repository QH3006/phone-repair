import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from backend.app.core.config import settings
from backend.app.db.init_db import init_db
from backend.app.api.endpoints import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Hệ thống Quản lý Trung tâm Sửa chữa Điện thoại Tích hợp AI (Giai đoạn KT1)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn Router API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Đường dẫn thư mục tĩnh & template Frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    templates = Jinja2Templates(directory=frontend_dir)

    @app.get("/", include_in_schema=False)
    def read_root(request: Request):
        return templates.TemplateResponse(request=request, name="index.html")

    @app.get("/tracking", include_in_schema=False)
    @app.get("/tra-cuu", include_in_schema=False)
    def read_customer_tracking(request: Request):
        """Cổng tra cứu tiến độ sửa chữa và bảo hành công khai riêng biệt dành cho khách hàng."""
        return templates.TemplateResponse(request=request, name="tracking.html")

@app.on_event("startup")
def on_startup():
    """Tự động khởi tạo database SQLite và nạp dữ liệu mẫu khi backend khởi động."""
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
