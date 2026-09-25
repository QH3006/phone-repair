"""
Module nạp dữ liệu mẫu thực tế 100% cho hệ thống PhoneCare AI.
Dữ liệu được quản lý tập trung tại seed_data.json để giữ code ngắn gọn, phân tách rõ ràng Code và Data.
"""
import os
import json
from datetime import datetime
from backend.app.db.models import (
    NguoiDung, KhachHang, ThietBi, LinhKien, DichVu, PhieuSuaChua,
    ChiTietSuaChua, HoaDon, BaoHanh, NhatKyAI
)
from backend.app.core.security import get_password_hash

JSON_PATH = os.path.join(os.path.dirname(__file__), "seed_data.json")

def parse_dt(val):
    if not val:
        return None
    try:
        return datetime.fromisoformat(val)
    except Exception:
        return None

def seed_realistic_data(db):
    """Nạp dữ liệu mẫu thực tế chuẩn thị trường sửa chữa Việt Nam."""
    if not os.path.exists(JSON_PATH):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu mẫu: {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Người dùng nhân sự (RBAC)
    users = [
        NguoiDung(ten_dang_nhap="admin", mat_khau_hash=get_password_hash("123456"), ho_ten="Nguyễn Hoàng Long", vai_tro="QuanLy", so_dien_thoai="0901112233"),
        NguoiDung(ten_dang_nhap="letan", mat_khau_hash=get_password_hash("123456"), ho_ten="Trần Mai Phương", vai_tro="LeTan", so_dien_thoai="0902223344"),
        NguoiDung(ten_dang_nhap="ktv", mat_khau_hash=get_password_hash("123456"), ho_ten="Lê Quốc Cường", vai_tro="KyThuatVien", so_dien_thoai="0903334455"),
        NguoiDung(ten_dang_nhap="ktv2", mat_khau_hash=get_password_hash("123456"), ho_ten="Vũ Đình Trọng", vai_tro="KyThuatVien", so_dien_thoai="0905556677"),
        NguoiDung(ten_dang_nhap="thungan", mat_khau_hash=get_password_hash("123456"), ho_ten="Phạm Thanh Hà", vai_tro="ThuNgan", so_dien_thoai="0904445566"),
    ]
    db.add_all(users)
    db.flush()

    # 2. Linh kiện & Dịch vụ
    db.add_all([LinhKien(**p) for p in data["parts"]])
    db.add_all([DichVu(**s) for s in data["services"]])
    db.flush()

    # 3. Khách hàng & Thiết bị
    for c in data["customers"]:
        db.add(KhachHang(id=c["id"], ho_ten=c["ho_ten"], so_dien_thoai=c["so_dien_thoai"], dia_chi=c["dia_chi"]))
    db.flush()

    for d in data["devices"]:
        db.add(ThietBi(
            id=d["id"], khach_hang_id=d["khach_hang_id"],
            hang_san_xuat=d["hang_san_xuat"], model_may=d["model_may"],
            so_imei=d["so_imei"], mat_khau_may=d.get("mat_khau_may")
        ))
    db.flush()

    # 4. Phiếu sửa chữa
    for t in data["tickets"]:
        db.add(PhieuSuaChua(
            id=t["id"], ma_phieu=t["ma_phieu"],
            khach_hang_id=t["khach_hang_id"], thiet_bi_id=t["thiet_bi_id"],
            ktv_id=t.get("ktv_id"), le_tan_id=t.get("le_tan_id"),
            mo_ta_loi_khach=t["mo_ta_loi_khach"], ghi_chu_ky_thuat=t.get("ghi_chu_ky_thuat"),
            ai_tom_tat_loi=t.get("ai_tom_tat_loi"), ai_giai_thich_dv=t.get("ai_giai_thich_dv"),
            trang_thai=t["trang_thai"], tong_tien_du_kien=t.get("tong_tien_du_kien", 0),
            ngay_tiep_nhan=parse_dt(t.get("ngay_tiep_nhan")),
            ngay_hen_tra=parse_dt(t.get("ngay_hen_tra")),
            ngay_hoan_tat=parse_dt(t.get("ngay_hoan_tat"))
        ))
    db.flush()

    # 5. Chi tiết, Hóa đơn, Bảo hành, Nhật ký AI
    db.add_all([ChiTietSuaChua(**dt) for dt in data["details"]])
    for inv in data["invoices"]:
        db.add(HoaDon(
            ma_hoa_don=inv["ma_hoa_don"], phieu_sua_chua_id=inv["phieu_sua_chua_id"],
            thu_ngan_id=inv["thu_ngan_id"], tong_tien=inv["tong_tien"],
            phuong_thuc_tt=inv.get("phuong_thuc_tt", "TienMat"),
            trang_thai_tt=inv.get("trang_thai_tt", "DaThanhToan"),
            ngay_thanh_toan=parse_dt(inv.get("ngay_thanh_toan"))
        ))
    for war in data["warranties"]:
        db.add(BaoHanh(
            ma_bao_hanh=war["ma_bao_hanh"], phieu_sua_chua_id=war["phieu_sua_chua_id"],
            linh_kien_id=war["linh_kien_id"], ngay_bat_dau=parse_dt(war.get("ngay_bat_dau")),
            ngay_het_han=parse_dt(war.get("ngay_het_han")), dieu_kien_bh=war.get("dieu_kien_bh"),
            trang_thai=war.get("trang_thai", "ConHan")
        ))
    for log in data["ai_logs"]:
        db.add(NhatKyAI(
            phieu_sua_chua_id=log.get("phieu_sua_chua_id"), loai_tac_vu=log["loai_tac_vu"],
            model_name=log.get("model_name", "gemini-1.5-flash"), prompt_input=log["prompt_input"],
            ai_raw_response=log.get("ai_raw_response"), ai_parsed_json=log.get("ai_parsed_json"),
            execution_time_ms=log.get("execution_time_ms"), trang_thai=log.get("trang_thai", "ThanhCong"),
            ngay_thuc_hien=parse_dt(log.get("ngay_thuc_hien"))
        ))

    db.commit()
