import sys
import os
import time
import pytest
from fastapi.testclient import TestClient

# Đảm bảo import được backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.main import app
from backend.app.db.init_db import init_db
from backend.app.db.database import SessionLocal
from backend.app.db.models import NguoiDung, KhachHang, ThietBi, LinhKien, DichVu, PhieuSuaChua

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def get_token_for_role(role_username: str):
    response = client.post("/api/auth/login", json={
        "ten_dang_nhap": role_username,
        "mat_khau": "123456"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

# ================= 1. AUTH & RBAC TESTS =================
def test_auth_login_success():
    res = client.post("/api/auth/login", json={"ten_dang_nhap": "admin", "mat_khau": "123456"})
    assert res.status_code == 200
    data = res.json()
    assert data["vai_tro"] == "QuanLy"
    assert "access_token" in data

def test_auth_login_fail():
    res = client.post("/api/auth/login", json={"ten_dang_nhap": "admin", "mat_khau": "wrongpass"})
    assert res.status_code == 401

def test_rbac_user_management():
    admin_token = get_token_for_role("admin")
    letan_token = get_token_for_role("letan")
    ts = int(time.time() * 1000)

    # 1. Admin (QuanLy) có quyền tạo User mới
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    res_create = client.post("/api/users", headers=headers_admin, json={
        "ten_dang_nhap": f"test_ktv_{ts}",
        "mat_khau": "123456",
        "ho_ten": "Vũ Đình Trọng",
        "vai_tro": "KyThuatVien",
        "so_dien_thoai": "0912345678"
    })
    assert res_create.status_code == 201
    new_user_id = res_create.json()["id"]

    # 2. LeTan không có quyền tạo User (phải bị chặn 403 Forbidden)
    headers_letan = {"Authorization": f"Bearer {letan_token}"}
    res_forbidden = client.post("/api/users", headers=headers_letan, json={
        "ten_dang_nhap": f"hacker_{ts}",
        "mat_khau": "123456",
        "ho_ten": "Hacker User",
        "vai_tro": "QuanLy"
    })
    assert res_forbidden.status_code == 403

    # 3. Admin xóa user vừa tạo
    res_del = client.delete(f"/api/users/{new_user_id}", headers=headers_admin)
    assert res_del.status_code == 200

# ================= 2. CUSTOMER & DEVICE CRUD TESTS =================
def test_customer_crud():
    admin_token = get_token_for_role("admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    ts = int(time.time() * 1000)
    phone = f"09{ts % 100000000:08d}"
    imei = f"35{ts}000"[:15]

    # Tạo khách hàng
    res = client.post("/api/customers", headers=headers, json={
        "ho_ten": "Trần Tuấn Kiệt",
        "so_dien_thoai": phone,
        "dia_chi": "Hà Nội"
    })
    assert res.status_code == 201
    cust_id = res.json()["id"]

    # Đọc chi tiết
    res_get = client.get(f"/api/customers/{cust_id}", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["ho_ten"] == "Trần Tuấn Kiệt"

    # Cập nhật
    res_put = client.put(f"/api/customers/{cust_id}", headers=headers, json={"dia_chi": "Đà Nẵng"})
    assert res_put.status_code == 200
    assert res_put.json()["dia_chi"] == "Đà Nẵng"

    # Đăng ký thiết bị cho khách
    res_dev = client.post("/api/devices", headers=headers, json={
        "khach_hang_id": cust_id,
        "hang_san_xuat": "Apple",
        "model_may": "iPhone 15 Pro",
        "so_imei": imei,
        "mat_khau_may": "9999"
    })
    assert res_dev.status_code == 201
    dev_id = res_dev.json()["id"]

    # Tra cứu thiết bị
    res_dev_get = client.get(f"/api/devices/{dev_id}", headers=headers)
    assert res_dev_get.status_code == 200
    assert res_dev_get.json()["model_may"] == "iPhone 15 Pro"

# ================= 3. INVENTORY & SERVICES CRUD TESTS =================
def test_part_and_service_crud():
    admin_token = get_token_for_role("admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    ts = int(time.time() * 1000)

    # Tạo linh kiện
    res_part = client.post("/api/parts", headers=headers, json={
        "ma_linh_kien": f"LK-TEST-{ts}",
        "ten_linh_kien": "Màn hình OLED Test",
        "loai_may": "iPhone 15",
        "gia_nhap": 1000000,
        "gia_ban": 1500000,
        "so_luong_ton": 10,
        "thoi_han_bao_hanh_thang": 12
    })
    assert res_part.status_code == 201
    part_id = res_part.json()["id"]

    # Tạo dịch vụ công
    res_srv = client.post("/api/services", headers=headers, json={
        "ma_dich_vu": f"DV-TEST-{ts}",
        "ten_dich_vu": "Công test kiểm tra toàn diện",
        "gia_cong": 100000,
        "mo_ta": "Kiểm tra 32 chức năng"
    })
    assert res_srv.status_code == 201
    srv_id = res_srv.json()["id"]

    # Cập nhật linh kiện
    res_part_up = client.put(f"/api/parts/{part_id}", headers=headers, json={"so_luong_ton": 8})
    assert res_part_up.status_code == 200
    assert res_part_up.json()["so_luong_ton"] == 8

# ================= 4. REPAIR TICKET LIFECYCLE & DETAILS =================
def test_repair_ticket_flow():
    letan_token = get_token_for_role("letan")
    ktv_token = get_token_for_role("ktv")
    thungan_token = get_token_for_role("thungan")
    ts = int(time.time() * 1000)
    phone = f"09{ts % 100000000:08d}"
    imei = f"86{ts}000"[:15]

    # 1. Lễ tân tiếp nhận máy
    res_intake = client.post("/api/repairs", headers={"Authorization": f"Bearer {letan_token}"}, json={
        "ho_ten": "Nguyễn Hải Đăng",
        "so_dien_thoai": phone,
        "dia_chi": "TP.HCM",
        "hang_san_xuat": "Samsung",
        "model_may": "Galaxy S23",
        "so_imei": imei,
        "mo_ta_loi_khach": "Hỏng chân sạc Type-C"
    })
    assert res_intake.status_code == 201
    phieu_id = res_intake.json()["phieu_id"]

    # 2. KTV kiểm tra & thêm linh kiện / dịch vụ
    # Lấy ID linh kiện mẫu có sẵn
    res_parts = client.get("/api/parts", headers={"Authorization": f"Bearer {ktv_token}"})
    assert res_parts.status_code == 200
    parts_list = res_parts.json()
    first_part = parts_list[0]

    res_add_item = client.post(f"/api/repairs/{phieu_id}/items", headers={"Authorization": f"Bearer {ktv_token}"}, json={
        "linh_kien_id": first_part["id"],
        "so_luong": 1
    })
    assert res_add_item.status_code == 201
    assert res_add_item.json()["thanh_tien"] == first_part["gia_ban"]

    # 3. KTV cập nhật trạng thái sang 'DaSuaXong'
    res_status = client.patch(f"/api/repairs/{phieu_id}/status", headers={"Authorization": f"Bearer {ktv_token}"}, json={
        "trang_thai": "DaSuaXong",
        "ghi_chu_ky_thuat": "Đã thay thế linh kiện và test sạc OK"
    })
    assert res_status.status_code == 200
    assert res_status.json()["trang_thai"] == "DaSuaXong"

    # 4. Thu ngân lập hóa đơn & tự động cấp bảo hành
    res_inv = client.post("/api/invoices", headers={"Authorization": f"Bearer {thungan_token}"}, json={
        "phieu_sua_chua_id": phieu_id,
        "phuong_thuc_tt": "ChuyenKhoan"
    })
    assert res_inv.status_code == 201
    inv_data = res_inv.json()
    assert inv_data["phuong_thuc_tt"] == "ChuyenKhoan"
    assert inv_data["tong_tien"] > 0

    # 5. Tra cứu bảo hành điện tử theo IMEI
    res_bh = client.get(f"/api/warranties/lookup?imei_or_phone={imei}")
    assert res_bh.status_code == 200
    bh_list = res_bh.json()
    assert len(bh_list) >= 1
    assert bh_list[0]["so_imei"] == imei

# ================= 5. DASHBOARD STATS TESTS =================
def test_dashboard_stats():
    admin_token = get_token_for_role("admin")
    res = client.get("/api/stats/overview", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert data["summary"]["total_repairs"] > 0
    assert "status_distribution" in data
    assert "top_models" in data

# ================= 6. PUBLIC LOOKUP & BACKUP TESTS =================
def test_public_repair_lookup():
    """Kiểm tra API tra cứu tiến độ sửa chữa công khai không cần token (FR-03 & UC_KH_Track)."""
    # Tra cứu bằng từ khóa "PSC"
    res = client.get("/api/repairs/lookup?q=PSC")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "ma_phieu" in data[0]
        assert "trang_thai" in data[0]

def test_database_backup_nfr08():
    """Kiểm tra cơ chế sao lưu tự động CSDL SQLite theo NFR-08."""
    import backup_db
    import os
    backup_file = backup_db.create_backup()
    assert os.path.exists(backup_file)
    assert os.path.getsize(backup_file) > 0

    backups = backup_db.list_backups()
    assert len(backups) >= 1
    assert any(b["path"] == backup_file for b in backups)

