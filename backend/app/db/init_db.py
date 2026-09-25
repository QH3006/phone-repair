from backend.app.db.database import engine, Base, SessionLocal
from backend.app.db.models import NguoiDung
from backend.app.db.seed_data import seed_realistic_data

def init_db():
    """Tạo bảng và nạp dữ liệu mẫu (Seed Data) chuẩn mực thực tế cho hệ thống."""
    print("--> Đang khởi tạo cấu trúc CSDL SQLite...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Kiểm tra xem đã có dữ liệu mẫu chưa
        if db.query(NguoiDung).first():
            print("--> CSDL đã có dữ liệu. Không cần nạp lại.")
            return

        print("--> Đang nạp dữ liệu mẫu thực tế chuẩn thị trường sửa chữa Việt Nam (Seed Data)...")
        seed_realistic_data(db)
        print("--> Đã nạp dữ liệu mẫu thực tế thành công 100%!")
    except Exception as e:
        db.rollback()
        print(f"--> Lỗi khởi tạo dữ liệu: {e}")
    finally:
        db.close()
