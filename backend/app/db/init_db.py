from datetime import datetime, timedelta
from backend.app.db.database import engine, Base, SessionLocal
from backend.app.db.models import (
    NguoiDung, KhachHang, ThietBi, LinhKien, DichVu, PhieuSuaChua,
    ChiTietSuaChua, HoaDon, BaoHanh, NhatKyAI
)
from backend.app.core.security import get_password_hash

def init_db():
    """Tạo bảng và nạp dữ liệu mẫu (Seed Data) chuẩn mực cho hệ thống."""
    print("--> Dang khoi tao cau truc CSDL SQLite...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Kiểm tra xem đã có dữ liệu mẫu chưa
        if db.query(NguoiDung).first():
            print("--> CSDL da co du lieu. Khong can nap lai.")
            return

        print("--> Dang nap du lieu mau (Seed Data)...")
        
        # 1. Tạo 4 Tài khoản nhân sự tương ứng 4 Vai trò (RBAC)
        # Mật khẩu mặc định: '123456'
        u_admin = NguoiDung(
            ten_dang_nhap="admin",
            mat_khau_hash=get_password_hash("123456"),
            ho_ten="Nguyễn Hoàng Long",
            vai_tro="QuanLy",
            so_dien_thoai="0901112233"
        )
        u_letan = NguoiDung(
            ten_dang_nhap="letan",
            mat_khau_hash=get_password_hash("123456"),
            ho_ten="Trần Mai Phương",
            vai_tro="LeTan",
            so_dien_thoai="0902223344"
        )
        u_ktv = NguoiDung(
            ten_dang_nhap="ktv",
            mat_khau_hash=get_password_hash("123456"),
            ho_ten="Lê Quốc Cường",
            vai_tro="KyThuatVien",
            so_dien_thoai="0903334455"
        )
        u_thungan = NguoiDung(
            ten_dang_nhap="thungan",
            mat_khau_hash=get_password_hash("123456"),
            ho_ten="Phạm Thanh Hà",
            vai_tro="ThuNgan",
            so_dien_thoai="0904445566"
        )
        db.add_all([u_admin, u_letan, u_ktv, u_thungan])
        db.flush()

        # 2. Khách hàng
        c1 = KhachHang(ho_ten="Hoàng Đức Minh", so_dien_thoai="0988123456", dia_chi="123 Cầu Giấy, Hà Nội")
        c2 = KhachHang(ho_ten="Nguyễn Thùy Linh", so_dien_thoai="0977234567", dia_chi="45 Hai Bà Trưng, Hà Nội")
        c3 = KhachHang(ho_ten="Phan Anh Tuấn", so_dien_thoai="0911345678", dia_chi="88 Nguyễn Trãi, Thanh Xuân, Hà Nội")
        db.add_all([c1, c2, c3])
        db.flush()

        # 3. Thiết bị của khách
        d1 = ThietBi(
            khach_hang_id=c1.id,
            hang_san_xuat="Apple",
            model_may="iPhone 13 Pro Max",
            so_imei="354892091234567",
            mat_khau_may="112233"
        )
        d2 = ThietBi(
            khach_hang_id=c2.id,
            hang_san_xuat="Samsung",
            model_may="Galaxy S22 Ultra",
            so_imei="359124089876543",
            mat_khau_may="000000"
        )
        d3 = ThietBi(
            khach_hang_id=c3.id,
            hang_san_xuat="Xiaomi",
            model_may="Redmi Note 12 Pro",
            so_imei="867530912384756",
            mat_khau_may="2580"
        )
        db.add_all([d1, d2, d3])
        db.flush()

        # 4. Linh kiện
        p1 = LinhKien(ma_linh_kien="LK-PIN-IP13PM", ten_linh_kien="Pin Zin Dung Lượng Cao iPhone 13 Pro Max", loai_may="iPhone 13 Pro Max", gia_nhap=450000, gia_ban=750000, so_luong_ton=15, thoi_han_bao_hanh_thang=12)
        p2 = LinhKien(ma_linh_kien="LK-MAN-S22U", ten_linh_kien="Màn hình Dynamic AMOLED 2X Galaxy S22 Ultra", loai_may="Galaxy S22 Ultra", gia_nhap=2800000, gia_ban=3600000, so_luong_ton=5, thoi_han_bao_hanh_thang=6)
        p3 = LinhKien(ma_linh_kien="LK-IC-U3300", ten_linh_kien="IC Quản Lý Sạc USB U3300 Chính Hãng", loai_may="iPhone Chung", gia_nhap=120000, gia_ban=350000, so_luong_ton=30, thoi_han_bao_hanh_thang=3)
        p4 = LinhKien(ma_linh_kien="LK-CAP-SAC-RN12", ten_linh_kien="Cụm Bo Cáp Sạc & Mic Redmi Note 12", loai_may="Redmi Note 12", gia_nhap=90000, gia_ban=220000, so_luong_ton=20, thoi_han_bao_hanh_thang=6)
        db.add_all([p1, p2, p3, p4])
        db.flush()

        # 5. Dịch vụ sửa chữa / Công thợ
        s1 = DichVu(ma_dich_vu="DV-THAY-PIN", ten_dich_vu="Công thay Pin & Test sạc xả an toàn", gia_cong=150000, mo_ta="Thay pin chuyên dụng, dán keo chống nước")
        s2 = DichVu(ma_dich_vu="DV-THAY-MAN", ten_dich_vu="Công ép kính / thay màn hình chuyên sâu", gia_cong=250000, mo_ta="Thao tác phòng sạch loại bỏ bụi")
        s3 = DichVu(ma_dich_vu="DV-SUA-NGUON", ten_dich_vu="Công xử lý chập nguồn mainboard chuyên sâu", gia_cong=350000, mo_ta="Dò chạm đường VDD_MAIN bằng camera nhiệt")
        db.add_all([s1, s2, s3])
        db.flush()

        # 6. Phiếu sửa chữa mẫu (Mỗi phiếu ở 1 trạng thái khác nhau)
        # Phiếu 1: Đang sửa chữa & có dữ liệu AI Tóm Tắt
        psc1 = PhieuSuaChua(
            ma_phieu="PSC-20260814-001",
            khach_hang_id=c1.id,
            thiet_bi_id=d1.id,
            le_tan_id=u_letan.id,
            ktv_id=u_ktv.id,
            mo_ta_loi_khach="Máy sập nguồn khi cắm sạc, pin tụt rất nhanh và nóng ran cạnh sườn.",
            ghi_chu_ky_thuat="Máy ngấm ẩm, chập đường VDD_MAIN do tụ C2301 rỉ sét. IC sạc USB U3300 nóng bất thường. Pin phù nhẹ 78% dung lượng.",
            ai_tom_tat_loi='{"hardware_issue": "Máy ngấm ẩm chập nguồn VDD_MAIN do tụ rỉ sét và hỏng IC sạc, pin phù chai", "faulty_components": ["Tụ C2301", "IC sạc USB U3300", "Pin"], "recommended_action": "Thay tụ C2301, thay IC sạc U3300 và thay pin Zin", "risk_level": "Cao"}',
            ai_giai_thich_dv="Thiết bị của bạn bị hỏng linh kiện điều phối dòng điện sạc giống như cầu chì trong nhà bị chập, khiến pin không thể nạp và nóng ran. Việc thay thế IC sạc và làm sạch tụ chập sẽ giúp nguồn điện ổn định, bảo vệ an toàn cho bo mạch chủ.",
            trang_thai="DangSuaChua",
            tong_tien_du_kien=1250000,
            ngay_tiep_nhan=datetime.utcnow() - timedelta(days=1),
            ngay_hen_tra=datetime.utcnow() + timedelta(hours=4)
        )

        # Phiếu 2: Đã sửa xong chờ thanh toán
        psc2 = PhieuSuaChua(
            ma_phieu="PSC-20260814-002",
            khach_hang_id=c2.id,
            thiet_bi_id=d2.id,
            le_tan_id=u_letan.id,
            ktv_id=u_ktv.id,
            mo_ta_loi_khach="Màn hình bị sọc xanh dọc thân máy sau khi va chạm góc bàn.",
            ghi_chu_ky_thuat="Tấm nền Dynamic AMOLED bị nứt cổ cáp hiển thị, cảm ứng góc phải liệt cục bộ. Cần thay nguyên cụm màn hình mới.",
            ai_tom_tat_loi='{"hardware_issue": "Màn hình AMOLED bị nứt cổ cáp và liệt cảm ứng cục bộ", "faulty_components": ["Cụm màn hình"], "recommended_action": "Thay cụm màn hình Dynamic AMOLED chính hãng", "risk_level": "TrungBinh"}',
            ai_giai_thich_dv="Màn hình điện thoại hoạt động như tấm gương điện tử, khi bị chấn động mạnh sẽ đứt các vi mạch siêu nhỏ dẫn đến sọc màn hình. Việc thay cụm màn hình mới sẽ khôi phục 100% độ sắc nét và độ nhạy cảm ứng.",
            trang_thai="DaSuaXong",
            tong_tien_du_kien=3850000,
            ngay_tiep_nhan=datetime.utcnow() - timedelta(hours=10),
            ngay_hen_tra=datetime.utcnow() + timedelta(hours=2)
        )

        # Phiếu 3: Mới tiếp nhận
        psc3 = PhieuSuaChua(
            ma_phieu="PSC-20260814-003",
            khach_hang_id=c3.id,
            thiet_bi_id=d3.id,
            le_tan_id=u_letan.id,
            ktv_id=None,
            mo_ta_loi_khach="Chân cắm sạc lỏng lẻo, phải bẻ gập dây sạc mới nhận dòng.",
            ghi_chu_ky_thuat=None,
            ai_tom_tat_loi=None,
            ai_giai_thich_dv=None,
            trang_thai="TiepNhan",
            tong_tien_du_kien=220000,
            ngay_tiep_nhan=datetime.utcnow()
        )
        db.add_all([psc1, psc2, psc3])
        db.flush()

        # 7. Chi tiết sửa chữa cho phiếu 1
        ct1 = ChiTietSuaChua(phieu_sua_chua_id=psc1.id, linh_kien_id=p1.id, dich_vu_id=None, so_luong=1, don_gia=750000, thanh_tien=750000)
        ct2 = ChiTietSuaChua(phieu_sua_chua_id=psc1.id, linh_kien_id=p3.id, dich_vu_id=None, so_luong=1, don_gia=350000, thanh_tien=350000)
        ct3 = ChiTietSuaChua(phieu_sua_chua_id=psc1.id, linh_kien_id=None, dich_vu_id=s3.id, so_luong=1, don_gia=150000, thanh_tien=150000)
        db.add_all([ct1, ct2, ct3])

        # 8. Hóa đơn & Bảo hành cho phiếu 2
        hd2 = HoaDon(
            ma_hoa_don="HD-20260814-001",
            phieu_sua_chua_id=psc2.id,
            thu_ngan_id=u_thungan.id,
            tong_tien=3850000,
            phuong_thuc_tt="ChuyenKhoan",
            trang_thai_tt="DaThanhToan"
        )
        bh2 = BaoHanh(
            ma_bao_hanh="BH-S22U-001",
            phieu_sua_chua_id=psc2.id,
            linh_kien_id=p2.id,
            ngay_bat_dau=datetime.utcnow(),
            ngay_het_han=datetime.utcnow() + timedelta(days=180),
            dieu_kien_bh="Bảo hành cảm ứng và hiển thị 6 tháng. Không bảo hành rơi vỡ, vào nước.",
            trang_thai="ConHan"
        )
        db.add_all([hd2, bh2])

        # 9. Nhật ký AI Log mẫu
        ai_log1 = NhatKyAI(
            phieu_sua_chua_id=psc1.id,
            loai_tac_vu="TomTatLoi",
            model_name="gemini-1.5-flash",
            prompt_input="[Prompt 5 Components] Ghi chú KTV: Máy ngấm ẩm, chập đường VDD_MAIN...",
            ai_raw_response=psc1.ai_tom_tat_loi,
            ai_parsed_json=psc1.ai_tom_tat_loi,
            execution_time_ms=1850.5,
            trang_thai="ThanhCong"
        )
        db.add(ai_log1)

        db.commit()
        print("--> Da nap du lieu mau (Seed Data) thanh cong 100%!")
    except Exception as e:
        db.rollback()
        print(f"--> Loi khoi tao du lieu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
