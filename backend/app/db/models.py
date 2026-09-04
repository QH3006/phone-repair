from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class NguoiDung(Base):
    """Bảng lưu thông tin tài khoản nhân viên và ban quản lý."""
    __tablename__ = "nguoi_dung"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ten_dang_nhap = Column(String(50), unique=True, index=True, nullable=False)
    mat_khau_hash = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    vai_tro = Column(String(30), nullable=False)  # 'QuanLy', 'LeTan', 'KyThuatVien', 'ThuNgan'
    so_dien_thoai = Column(String(15), nullable=True)
    trang_thai = Column(String(20), default="HoatDong")
    ngay_tao = Column(DateTime, default=datetime.utcnow)

    # Relationships
    phieu_tiep_nhan = relationship("PhieuSuaChua", foreign_keys="PhieuSuaChua.le_tan_id", back_populates="le_tan")
    phieu_sua_chua = relationship("PhieuSuaChua", foreign_keys="PhieuSuaChua.ktv_id", back_populates="ktv")
    hoa_don = relationship("HoaDon", back_populates="thu_ngan")


class KhachHang(Base):
    """Bảng quản lý hồ sơ thông tin khách hàng."""
    __tablename__ = "khach_hang"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ho_ten = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(15), unique=True, index=True, nullable=False)
    dia_chi = Column(String(255), nullable=True)
    ngay_tao = Column(DateTime, default=datetime.utcnow)

    # Relationships
    thiet_bi = relationship("ThietBi", back_populates="khach_hang", cascade="all, delete-orphan")
    phieu_sua_chua = relationship("PhieuSuaChua", back_populates="khach_hang")


class ThietBi(Base):
    """Bảng lưu trữ thông tin phần cứng thiết bị của khách hàng."""
    __tablename__ = "thiet_bi"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    khach_hang_id = Column(Integer, ForeignKey("khach_hang.id", ondelete="CASCADE"), nullable=False)
    hang_san_xuat = Column(String(50), nullable=False)
    model_may = Column(String(100), nullable=False)
    so_imei = Column(String(30), unique=True, index=True, nullable=False)
    mat_khau_may = Column(String(50), nullable=True)
    ngay_tao = Column(DateTime, default=datetime.utcnow)

    # Relationships
    khach_hang = relationship("KhachHang", back_populates="thiet_bi")
    phieu_sua_chua = relationship("PhieuSuaChua", back_populates="thiet_bi")


class LinhKien(Base):
    """Bảng danh mục linh kiện thay thế và tồn kho."""
    __tablename__ = "linh_kien"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_linh_kien = Column(String(50), unique=True, index=True, nullable=False)
    ten_linh_kien = Column(String(150), nullable=False)
    loai_may = Column(String(100), nullable=True)
    gia_nhap = Column(Float, nullable=False)
    gia_ban = Column(Float, nullable=False)
    so_luong_ton = Column(Integer, default=0, nullable=False)
    thoi_han_bao_hanh_thang = Column(Integer, default=6)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chi_tiet = relationship("ChiTietSuaChua", back_populates="linh_kien")
    bao_hanh = relationship("BaoHanh", back_populates="linh_kien")


class DichVu(Base):
    """Bảng danh mục dịch vụ kỹ thuật / bảng giá công sửa chữa."""
    __tablename__ = "dich_vu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_dich_vu = Column(String(50), unique=True, index=True, nullable=False)
    ten_dich_vu = Column(String(150), nullable=False)
    gia_cong = Column(Float, nullable=False)
    mo_ta = Column(Text, nullable=True)

    # Relationships
    chi_tiet = relationship("ChiTietSuaChua", back_populates="dich_vu")


class PhieuSuaChua(Base):
    """Thực thể trung tâm quản lý toàn bộ vòng đời phiếu sửa chữa (8 trạng thái)."""
    __tablename__ = "phieu_sua_chua"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_phieu = Column(String(30), unique=True, index=True, nullable=False)
    khach_hang_id = Column(Integer, ForeignKey("khach_hang.id"), nullable=False)
    thiet_bi_id = Column(Integer, ForeignKey("thiet_bi.id"), nullable=False)
    le_tan_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    ktv_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=True)
    
    mo_ta_loi_khach = Column(Text, nullable=False)
    ghi_chu_ky_thuat = Column(Text, nullable=True)
    hinh_anh = Column(Text, nullable=True)  # URL hoặc Base64 ảnh thiết bị khi tiếp nhận
    ai_tom_tat_loi = Column(Text, nullable=True)  # Bản tóm tắt dạng JSON/Markdown
    ai_giai_thich_dv = Column(Text, nullable=True)  # Giải thích đời thường cho khách
    
    # 8 Trạng thái chuẩn hóa
    trang_thai = Column(String(30), default="TiepNhan", nullable=False)
    tong_tien_du_kien = Column(Float, default=0.0)
    
    ngay_tiep_nhan = Column(DateTime, default=datetime.utcnow)
    ngay_hen_tra = Column(DateTime, nullable=True)
    ngay_hoan_tat = Column(DateTime, nullable=True)

    # Relationships
    khach_hang = relationship("KhachHang", back_populates="phieu_sua_chua")
    thiet_bi = relationship("ThietBi", back_populates="phieu_sua_chua")
    le_tan = relationship("NguoiDung", foreign_keys=[le_tan_id], back_populates="phieu_tiep_nhan")
    ktv = relationship("NguoiDung", foreign_keys=[ktv_id], back_populates="phieu_sua_chua")
    
    chi_tiet = relationship("ChiTietSuaChua", back_populates="phieu_sua_chua", cascade="all, delete-orphan")
    hoa_don = relationship("HoaDon", back_populates="phieu_sua_chua", uselist=False)
    bao_hanh = relationship("BaoHanh", back_populates="phieu_sua_chua")
    nhat_ky_ai = relationship("NhatKyAI", back_populates="phieu_sua_chua")


class ChiTietSuaChua(Base):
    """Chi tiết các linh kiện và dịch vụ áp dụng cho phiếu sửa chữa."""
    __tablename__ = "chi_tiet_sua_chua"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phieu_sua_chua_id = Column(Integer, ForeignKey("phieu_sua_chua.id", ondelete="CASCADE"), nullable=False)
    linh_kien_id = Column(Integer, ForeignKey("linh_kien.id"), nullable=True)
    dich_vu_id = Column(Integer, ForeignKey("dich_vu.id"), nullable=True)
    so_luong = Column(Integer, default=1)
    don_gia = Column(Float, nullable=False)
    thanh_tien = Column(Float, nullable=False)

    # Relationships
    phieu_sua_chua = relationship("PhieuSuaChua", back_populates="chi_tiet")
    linh_kien = relationship("LinhKien", back_populates="chi_tiet")
    dich_vu = relationship("DichVu", back_populates="chi_tiet")


class HoaDon(Base):
    """Bảng hóa đơn thanh toán cho phiếu sửa chữa."""
    __tablename__ = "hoa_don"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_hoa_don = Column(String(30), unique=True, index=True, nullable=False)
    phieu_sua_chua_id = Column(Integer, ForeignKey("phieu_sua_chua.id"), unique=True, nullable=False)
    thu_ngan_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    tong_tien = Column(Float, nullable=False)
    phuong_thuc_tt = Column(String(30), default="TienMat")  # 'TienMat', 'ChuyenKhoan'
    trang_thai_tt = Column(String(30), default="DaThanhToan")
    ngay_thanh_toan = Column(DateTime, default=datetime.utcnow)

    # Relationships
    phieu_sua_chua = relationship("PhieuSuaChua", back_populates="hoa_don")
    thu_ngan = relationship("NguoiDung", back_populates="hoa_don")


class BaoHanh(Base):
    """Bảng quản lý bảo hành điện tử sau sửa chữa."""
    __tablename__ = "bao_hanh"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_bao_hanh = Column(String(30), unique=True, index=True, nullable=False)
    phieu_sua_chua_id = Column(Integer, ForeignKey("phieu_sua_chua.id"), nullable=False)
    linh_kien_id = Column(Integer, ForeignKey("linh_kien.id"), nullable=False)
    ngay_bat_dau = Column(DateTime, default=datetime.utcnow)
    ngay_het_han = Column(DateTime, nullable=False)
    dieu_kien_bh = Column(Text, nullable=True)
    trang_thai = Column(String(20), default="ConHan")  # 'ConHan', 'HetHan', 'TuChoi'

    # Relationships
    phieu_sua_chua = relationship("PhieuSuaChua", back_populates="bao_hanh")
    linh_kien = relationship("LinhKien", back_populates="bao_hanh")


class NhatKyAI(Base):
    """Bảng lưu vết toàn bộ hoạt động gọi AI phục vụ kiểm tra, truy vết và phân tích."""
    __tablename__ = "nhat_ky_ai"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phieu_sua_chua_id = Column(Integer, ForeignKey("phieu_sua_chua.id", ondelete="SET NULL"), nullable=True)
    loai_tac_vu = Column(String(50), nullable=False)  # 'TomTatLoi', 'SinhTinNhan', 'GiaiThichDichVu'
    model_name = Column(String(50), default="gemini-1.5-flash")
    prompt_input = Column(Text, nullable=False)
    ai_raw_response = Column(Text, nullable=True)
    ai_parsed_json = Column(Text, nullable=True)
    execution_time_ms = Column(Float, nullable=True)
    trang_thai = Column(String(30), default="ThanhCong")  # 'ThanhCong', 'Fallback', 'Loi'
    ngay_thuc_hien = Column(DateTime, default=datetime.utcnow)

    # Relationships
    phieu_sua_chua = relationship("PhieuSuaChua", back_populates="nhat_ky_ai")
