# ==============================================================
# Dockerfile: Hệ thống Quản lý Sửa chữa Điện thoại AI (PhoneCare AI)
# Multi-stage / Lightweight Production Python Image
# ==============================================================

FROM python:3.12-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Ngăn Python tạo file .pyc và bật unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Cài đặt curl phục vụ kiểm tra sức khỏe container (Healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Tận dụng Docker layer cache: Cài đặt thư viện trước
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY scripts/ ./scripts/
COPY pytest.ini ./

# Mở cổng dịch vụ
EXPOSE 8000

# Kiểm tra sức khỏe ứng dụng
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Khởi chạy ứng dụng qua Uvicorn trên 0.0.0.0:8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
