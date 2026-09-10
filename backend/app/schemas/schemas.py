from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Dict
from datetime import datetime

# ================= AUTH SCHEMAS =================
class LoginRequest(BaseModel):
    ten_dang_nhap: str
    mat_khau: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id: int
    ho_ten: str
    vai_tro: str
    ten_dang_nhap: str
    so_dien_thoai: Optional[str] = None

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    mat_khau_cu: str
    mat_khau_moi: str

# ================= USER SCHEMAS (RBAC) =================
class UserBase(BaseModel):
    ten_dang_nhap: str
    ho_ten: str
    vai_tro: str = Field(..., description="QuanLy, LeTan, KyThuatVien, ThuNgan")
    so_dien_thoai: Optional[str] = None
    trang_thai: Optional[str] = "HoatDong"

class UserCreate(UserBase):
    mat_khau: str

class UserUpdate(BaseModel):
    ho_ten: Optional[str] = None
    vai_tro: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    trang_thai: Optional[str] = None
    mat_khau: Optional[str] = None

class UserOut(UserBase):
    id: int
    ngay_tao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# ================= CUSTOMER SCHEMAS =================
class CustomerBase(BaseModel):
    ho_ten: str
    so_dien_thoai: str
    dia_chi: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    ho_ten: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    ngay_tao: Optional[datetime] = None
    so_thiet_bi: Optional[int] = 0
    so_phieu_sua: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

# ================= DEVICE SCHEMAS =================
class DeviceBase(BaseModel):
    khach_hang_id: int
    hang_san_xuat: str
    model_may: str
    so_imei: str
    mat_khau_may: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    hang_san_xuat: Optional[str] = None
    model_may: Optional[str] = None
    so_imei: Optional[str] = None
    mat_khau_may: Optional[str] = None

class DeviceOut(DeviceBase):
    id: int
    ngay_tao: Optional[datetime] = None
    ten_khach_hang: Optional[str] = None
    so_dien_thoai_khach: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# ================= INVENTORY / PART SCHEMAS =================
class PartBase(BaseModel):
    ma_linh_kien: str
    ten_linh_kien: str
    loai_may: Optional[str] = None
    gia_nhap: float = Field(..., ge=0)
    gia_ban: float = Field(..., ge=0)
    so_luong_ton: int = Field(0, ge=0)
    thoi_han_bao_hanh_thang: int = Field(6, ge=0)

class PartCreate(PartBase):
    pass

class PartUpdate(BaseModel):
    ma_linh_kien: Optional[str] = None
    ten_linh_kien: Optional[str] = None
    loai_may: Optional[str] = None
    gia_nhap: Optional[float] = None
    gia_ban: Optional[float] = None
    so_luong_ton: Optional[int] = None
    thoi_han_bao_hanh_thang: Optional[int] = None

class PartOut(PartBase):
    id: int
    ngay_cap_nhat: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# ================= SERVICE CATALOG SCHEMAS =================
class ServiceBase(BaseModel):
    ma_dich_vu: str
    ten_dich_vu: str
    gia_cong: float = Field(..., ge=0)
    mo_ta: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    ma_dich_vu: Optional[str] = None
    ten_dich_vu: Optional[str] = None
    gia_cong: Optional[float] = None
    mo_ta: Optional[str] = None

class ServiceOut(ServiceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ================= REPAIR DETAIL (ITEMS) SCHEMAS =================
class RepairDetailCreate(BaseModel):
    linh_kien_id: Optional[int] = None
    dich_vu_id: Optional[int] = None
    so_luong: int = Field(1, ge=1)
    don_gia: Optional[float] = None

class RepairDetailOut(BaseModel):
    id: int
    phieu_sua_chua_id: int
    linh_kien_id: Optional[int] = None
    dich_vu_id: Optional[int] = None
    ten_muc: str
    loai: str  # 'LinhKien' or 'DichVu'
    so_luong: int
    don_gia: float
    thanh_tien: float

    model_config = ConfigDict(from_attributes=True)

# ================= REPAIR TICKET SCHEMAS =================
class CreateRepairTicketRequest(BaseModel):
    ho_ten: str = Field(..., examples=["Hoàng Đức Minh"])
    so_dien_thoai: str = Field(..., examples=["0988123456"])
    dia_chi: Optional[str] = Field(None, examples=["123 Cầu Giấy, Hà Nội"])
    hang_san_xuat: str = Field(..., examples=["Apple"])
    model_may: str = Field(..., examples=["iPhone 14 Pro Max"])
    so_imei: Optional[str] = Field(None, examples=["354892091234567"])
    mat_khau_may: Optional[str] = Field(None, examples=["112233"])
    mo_ta_loi_khach: str = Field(..., examples=["Màn hình nứt vỡ, cảm ứng đơ"])
    ghi_chu_ky_thuat: Optional[str] = None
    tong_tien_du_kien: Optional[float] = 0.0
    hinh_anh: Optional[str] = None
    le_tan_id: Optional[int] = None
    ktv_id: Optional[int] = None
    ngay_hen_tra: Optional[datetime] = None

class UpdateRepairStatusRequest(BaseModel):
    trang_thai: str = Field(..., examples=["DangKiemTra"])
    ghi_chu_ky_thuat: Optional[str] = None
    ktv_id: Optional[int] = None
    tong_tien_du_kien: Optional[float] = None

class AssignKTVRequest(BaseModel):
    ktv_id: int

class RepairTicketOut(BaseModel):
    id: int
    ma_phieu: str
    khach_hang_id: int
    thiet_bi_id: int
    khach_hang: Dict[str, Any]
    thiet_bi: Dict[str, Any]
    mo_ta_loi_khach: str
    ghi_chu_ky_thuat: Optional[str] = None
    hinh_anh: Optional[str] = None
    ai_tom_tat_loi: Optional[str] = None
    ai_giai_thich_dv: Optional[str] = None
    trang_thai: str
    tong_tien_du_kien: float
    ktv_id: Optional[int] = None
    ktv_phu_trach: str
    le_tan_id: Optional[int] = None
    le_tan_tiep_nhan: str
    ngay_tiep_nhan: Optional[str] = None
    ngay_hen_tra: Optional[str] = None
    ngay_hoan_tat: Optional[str] = None
    chi_tiet: List[RepairDetailOut] = []
    da_thanh_toan: bool = False
    co_bao_hanh: bool = False

# ================= INVOICE SCHEMAS =================
class InvoiceCreate(BaseModel):
    phieu_sua_chua_id: int
    phuong_thuc_tt: str = Field("TienMat", description="'TienMat' hoặc 'ChuyenKhoan'")
    ghi_chu: Optional[str] = None

class InvoiceOut(BaseModel):
    id: int
    ma_hoa_don: str
    phieu_sua_chua_id: int
    ma_phieu: str
    ten_khach_hang: str
    so_dien_thoai: str
    model_may: str
    thu_ngan_id: int
    thu_ngan_ten: str
    tong_tien: float
    phuong_thuc_tt: str
    trang_thai_tt: str
    ngay_thanh_toan: Optional[str] = None
    chi_tiet_items: List[Dict[str, Any]] = []

    model_config = ConfigDict(from_attributes=True)

# ================= WARRANTY SCHEMAS =================
class WarrantyCreate(BaseModel):
    phieu_sua_chua_id: int
    linh_kien_id: int
    thoi_han_thang: Optional[int] = 6
    dieu_kien_bh: Optional[str] = None

class WarrantyOut(BaseModel):
    id: int
    ma_bao_hanh: str
    phieu_sua_chua_id: int
    ma_phieu: str
    ten_khach_hang: str
    so_dien_thoai: str
    model_may: str
    so_imei: str
    ten_linh_kien: str
    ngay_bat_dau: Optional[str] = None
    ngay_het_han: Optional[str] = None
    dieu_kien_bh: Optional[str] = None
    trang_thai: str

    model_config = ConfigDict(from_attributes=True)

# ================= AI SCHEMAS =================
class FaultSummaryRequest(BaseModel):
    phieu_id: Optional[int] = None
    model_may: str = Field(..., examples=["iPhone 13 Pro Max"])
    mo_ta_loi_khach: str = Field(..., examples=["Máy sập nguồn khi cắm sạc, máy nóng ran"])
    ghi_chu_ky_thuat: str = Field(..., examples=["Chập đường VDD_MAIN do rỉ sét tụ C2301, IC sạc U3300 nóng bất thường"])

class ProgressMessageRequest(BaseModel):
    phieu_id: Optional[int] = None
    ten_khach: str = Field(..., examples=["Hoàng Đức Minh"])
    model_may: str = Field(..., examples=["iPhone 13 Pro Max"])
    trang_thai: str = Field(..., examples=["DaSuaXong"])
    chi_phi: float = Field(..., examples=[1250000])
    ngay_hen: str = Field(..., examples=["Trước 18h hôm nay"])
    kenh_gui: str = Field(default="SMS", examples=["SMS"])

class ServiceExplainRequest(BaseModel):
    phieu_id: Optional[int] = None
    ten_dich_vu: str = Field(..., examples=["Xử lý chập nguồn mainboard"])
    ten_linh_kien: str = Field(..., examples=["IC Sạc USB U3300 & Tụ lọc"])
    loi_thuc_te: str = Field(..., examples=["Máy cắm sạc không lên nguồn, sườn máy nóng ran"])

class ApproveAIDataRequest(BaseModel):
    phieu_id: int
    ai_tom_tat_loi: Optional[str] = None
    ai_giai_thich_dv: Optional[str] = None
    ghi_chu_ky_thuat: Optional[str] = None
    trang_thai_moi: Optional[str] = None
