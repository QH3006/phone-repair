"""
Script tiện ích làm mới và tái nạp CSDL PhoneCare AI theo dữ liệu thực tế.
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Đảm bảo đường dẫn import
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app.db.database import engine, Base, SessionLocal
from backend.app.db.seed_data import seed_realistic_data

def reseed_database():
    print("--> Dang khoi tao lai cau truc CSDL SQLite...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("--> Dang nap du lieu mau tu seed_data.json...")
        seed_realistic_data(db)
        print("--> Tai tao CSDL thuc te thanh cong 100%!")
    except Exception as e:
        db.rollback()
        print(f"--> Lỗi khi nạp dữ liệu: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    reseed_database()
