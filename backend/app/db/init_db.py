from backend.app.db.database import engine, Base, SessionLocal
from backend.app.db.models import NguoiDung
from backend.app.db.seed_data import seed_realistic_data

def _safe_print(msg: str):
    try:
        print(msg)
    except Exception:
        pass

def init_db():
    """Tạo bảng và nạp dữ liệu mẫu (Seed Data) chuẩn mực thực tế cho hệ thống."""
    _safe_print("--> Đang khởi tạo cấu trúc CSDL SQLite...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Kiểm tra xem đã có dữ liệu mẫu chưa
        if db.query(NguoiDung).first():
            _safe_print("--> CSDL đã có dữ liệu. Không cần nạp lại.")
            return

        _safe_print("--> Đang nạp dữ liệu mẫu thực tế chuẩn thị trường sửa chữa Việt Nam (Seed Data)...")
        seed_realistic_data(db)
        _safe_print("--> Đã nạp dữ liệu mẫu thực tế thành công 100%!")
    except Exception as e:
        db.rollback()
        _safe_print(f"--> Lỗi khởi tạo dữ liệu: {e}")
    finally:
        db.close()
