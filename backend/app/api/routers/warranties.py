from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from backend.app.db.database import get_db
from backend.app.db.models import BaoHanh, PhieuSuaChua, LinhKien, NguoiDung, ThietBi, KhachHang
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import WarrantyCreate, WarrantyOut

router = APIRouter(prefix="/warranties", tags=["Quản lý Bảo Hành Điện Tử"])

@router.get("", response_model=List[WarrantyOut])
def list_warranties(
    q: Optional[str] = Query(None, description="Tra cứu theo Mã BH, IMEI, SĐT hoặc Tên khách"),
    trang_thai: Optional[str] = Query(None, description="Lọc theo trạng thái ConHan / HetHan / TuChoi"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách các phiếu bảo hành điện tử hoặc tra cứu bảo hành."""
    query = db.query(BaoHanh)
    if trang_thai:
        query = query.filter(BaoHanh.trang_thai == trang_thai)
    
    if q:
        search = f"%{q.strip()}%"
        query = query.join(BaoHanh.phieu_sua_chua).join(PhieuSuaChua.khach_hang).join(PhieuSuaChua.thiet_bi).filter(
            (BaoHanh.ma_bao_hanh.ilike(search)) |
            (KhachHang.so_dien_thoai.ilike(search)) |
            (KhachHang.ho_ten.ilike(search)) |
            (ThietBi.so_imei.ilike(search))
        )
    
    warranties = query.order_by(BaoHanh.id.desc()).offset(skip).limit(limit).all()
    result = []
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    for bh in warranties:
        p = bh.phieu_sua_chua
        # Tự động cập nhật trạng thái nếu đã hết hạn
        status_bh = bh.trang_thai
        if bh.ngay_het_han and bh.ngay_het_han < now and status_bh == "ConHan":
            status_bh = "HetHan"
            bh.trang_thai = "HetHan"
            db.commit()

        result.append(WarrantyOut(
            id=bh.id,
            ma_bao_hanh=bh.ma_bao_hanh,
            phieu_sua_chua_id=bh.phieu_sua_chua_id,
            ma_phieu=p.ma_phieu if p else "N/A",
            ten_khach_hang=p.khach_hang.ho_ten if (p and p.khach_hang) else "N/A",
            so_dien_thoai=p.khach_hang.so_dien_thoai if (p and p.khach_hang) else "N/A",
            model_may=p.thiet_bi.model_may if (p and p.thiet_bi) else "N/A",
            so_imei=p.thiet_bi.so_imei if (p and p.thiet_bi) else "N/A",
            ten_linh_kien=bh.linh_kien.ten_linh_kien if bh.linh_kien else "Linh kiện khác",
            ngay_bat_dau=bh.ngay_bat_dau.strftime("%d/%m/%Y") if bh.ngay_bat_dau else None,
            ngay_het_han=bh.ngay_het_han.strftime("%d/%m/%Y") if bh.ngay_het_han else None,
            dieu_kien_bh=bh.dieu_kien_bh,
            trang_thai=status_bh
        ))
    return result

@router.get("/lookup", response_model=List[WarrantyOut])
def lookup_warranty(
    imei_or_phone: str = Query(..., description="Số IMEI thiết bị hoặc Số điện thoại"),
    db: Session = Depends(get_db)
):
    """Tra cứu bảo hành công khai cho khách hàng không cần đăng nhập."""
    search = f"%{imei_or_phone.strip()}%"
    warranties = db.query(BaoHanh).join(BaoHanh.phieu_sua_chua).join(PhieuSuaChua.khach_hang).join(PhieuSuaChua.thiet_bi).filter(
        (ThietBi.so_imei.ilike(search)) |
        (KhachHang.so_dien_thoai.ilike(search)) |
        (BaoHanh.ma_bao_hanh.ilike(search))
    ).all()

    result = []
    for bh in warranties:
        p = bh.phieu_sua_chua
        result.append(WarrantyOut(
            id=bh.id,
            ma_bao_hanh=bh.ma_bao_hanh,
            phieu_sua_chua_id=bh.phieu_sua_chua_id,
            ma_phieu=p.ma_phieu if p else "N/A",
            ten_khach_hang=p.khach_hang.ho_ten if (p and p.khach_hang) else "N/A",
            so_dien_thoai=p.khach_hang.so_dien_thoai if (p and p.khach_hang) else "N/A",
            model_may=p.thiet_bi.model_may if (p and p.thiet_bi) else "N/A",
            so_imei=p.thiet_bi.so_imei if (p and p.thiet_bi) else "N/A",
            ten_linh_kien=bh.linh_kien.ten_linh_kien if bh.linh_kien else "Linh kiện khác",
            ngay_bat_dau=bh.ngay_bat_dau.strftime("%d/%m/%Y") if bh.ngay_bat_dau else None,
            ngay_het_han=bh.ngay_het_han.strftime("%d/%m/%Y") if bh.ngay_het_han else None,
            dieu_kien_bh=bh.dieu_kien_bh,
            trang_thai=bh.trang_thai
        ))
    return result

@router.post("", response_model=WarrantyOut, status_code=status.HTTP_201_CREATED)
def create_warranty(
    req: WarrantyCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "ThuNgan", "KyThuatVien"]))
):
    """Cấp mới phiếu bảo hành điện tử thủ công."""
    p = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == req.phieu_sua_chua_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    lk = db.query(LinhKien).filter(LinhKien.id == req.linh_kien_id).first()
    if not lk:
        raise HTTPException(status_code=404, detail="Không tìm thấy linh kiện.")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    today_str = now.strftime("%Y%m%d")
    count_bh = db.query(BaoHanh).count()
    ma_bh = f"BH-{today_str}-{count_bh + 1:03d}"

    thoi_han = req.thoi_han_thang or lk.thoi_han_bao_hanh_thang or 6
    bh = BaoHanh(
        ma_bao_hanh=ma_bh,
        phieu_sua_chua_id=p.id,
        linh_kien_id=lk.id,
        ngay_bat_dau=now,
        ngay_het_han=now + timedelta(days=thoi_han * 30),
        dieu_kien_bh=req.dieu_kien_bh or f"Bảo hành {thoi_han} tháng cho {lk.ten_linh_kien}.",
        trang_thai="ConHan"
    )
    db.add(bh)
    db.commit()
    db.refresh(bh)

    return WarrantyOut(
        id=bh.id,
        ma_bao_hanh=bh.ma_bao_hanh,
        phieu_sua_chua_id=bh.phieu_sua_chua_id,
        ma_phieu=p.ma_phieu,
        ten_khach_hang=p.khach_hang.ho_ten if p.khach_hang else "N/A",
        so_dien_thoai=p.khach_hang.so_dien_thoai if p.khach_hang else "N/A",
        model_may=p.thiet_bi.model_may if p.thiet_bi else "N/A",
        so_imei=p.thiet_bi.so_imei if p.thiet_bi else "N/A",
        ten_linh_kien=lk.ten_linh_kien,
        ngay_bat_dau=bh.ngay_bat_dau.strftime("%d/%m/%Y"),
        ngay_het_han=bh.ngay_het_han.strftime("%d/%m/%Y"),
        dieu_kien_bh=bh.dieu_kien_bh,
        trang_thai=bh.trang_thai
    )
