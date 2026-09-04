from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.db.models import ThietBi, KhachHang, NguoiDung
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import DeviceCreate, DeviceUpdate, DeviceOut

router = APIRouter(prefix="/devices", tags=["Quản lý Thiết bị"])

@router.get("", response_model=List[DeviceOut])
def list_devices(
    khach_hang_id: Optional[int] = None,
    q: Optional[str] = Query(None, description="Tìm kiếm theo IMEI hoặc Model máy"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách thiết bị kèm thông tin chủ sở hữu."""
    query = db.query(ThietBi)
    if khach_hang_id:
        query = query.filter(ThietBi.khach_hang_id == khach_hang_id)
    if q:
        search = f"%{q.strip()}%"
        query = query.filter((ThietBi.so_imei.ilike(search)) | (ThietBi.model_may.ilike(search)))
    
    devices = query.order_by(ThietBi.id.desc()).offset(skip).limit(limit).all()
    result = []
    for d in devices:
        result.append(DeviceOut(
            id=d.id,
            khach_hang_id=d.khach_hang_id,
            hang_san_xuat=d.hang_san_xuat,
            model_may=d.model_may,
            so_imei=d.so_imei,
            mat_khau_may=d.mat_khau_may,
            ngay_tao=d.ngay_tao,
            ten_khach_hang=d.khach_hang.ho_ten if d.khach_hang else "N/A",
            so_dien_thoai_khach=d.khach_hang.so_dien_thoai if d.khach_hang else "N/A"
        ))
    return result

@router.get("/{device_id}", response_model=DeviceOut)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xem chi tiết một thiết bị."""
    d = db.query(ThietBi).filter(ThietBi.id == device_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Không tìm thấy thiết bị.")
    return DeviceOut(
        id=d.id,
        khach_hang_id=d.khach_hang_id,
        hang_san_xuat=d.hang_san_xuat,
        model_may=d.model_may,
        so_imei=d.so_imei,
        mat_khau_may=d.mat_khau_may,
        ngay_tao=d.ngay_tao,
        ten_khach_hang=d.khach_hang.ho_ten if d.khach_hang else "N/A",
        so_dien_thoai_khach=d.khach_hang.so_dien_thoai if d.khach_hang else "N/A"
    )

@router.post("", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(
    req: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan", "KyThuatVien"]))
):
    """Đăng ký thiết bị mới cho khách hàng."""
    kh = db.query(KhachHang).filter(KhachHang.id == req.khach_hang_id).first()
    if not kh:
        raise HTTPException(status_code=404, detail="Khách hàng không tồn tại.")
    
    existing = db.query(ThietBi).filter(ThietBi.so_imei == req.so_imei.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Số IMEI này đã được đăng ký cho thiết bị khác.")

    d = ThietBi(
        khach_hang_id=req.khach_hang_id,
        hang_san_xuat=req.hang_san_xuat.strip(),
        model_may=req.model_may.strip(),
        so_imei=req.so_imei.strip(),
        mat_khau_may=req.mat_khau_may.strip() if req.mat_khau_may else None
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return DeviceOut(
        id=d.id,
        khach_hang_id=d.khach_hang_id,
        hang_san_xuat=d.hang_san_xuat,
        model_may=d.model_may,
        so_imei=d.so_imei,
        mat_khau_may=d.mat_khau_may,
        ngay_tao=d.ngay_tao,
        ten_khach_hang=kh.ho_ten,
        so_dien_thoai_khach=kh.so_dien_thoai
    )

@router.put("/{device_id}", response_model=DeviceOut)
def update_device(
    device_id: int,
    req: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan", "KyThuatVien"]))
):
    """Cập nhật thông tin thiết bị."""
    d = db.query(ThietBi).filter(ThietBi.id == device_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Không tìm thấy thiết bị.")

    if req.so_imei and req.so_imei.strip() != d.so_imei:
        existing = db.query(ThietBi).filter(ThietBi.so_imei == req.so_imei.strip()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Số IMEI mới bị trùng với thiết bị khác.")
        d.so_imei = req.so_imei.strip()

    if req.hang_san_xuat is not None:
        d.hang_san_xuat = req.hang_san_xuat.strip()
    if req.model_may is not None:
        d.model_may = req.model_may.strip()
    if req.mat_khau_may is not None:
        d.mat_khau_may = req.mat_khau_may.strip()

    db.commit()
    db.refresh(d)
    return DeviceOut(
        id=d.id,
        khach_hang_id=d.khach_hang_id,
        hang_san_xuat=d.hang_san_xuat,
        model_may=d.model_may,
        so_imei=d.so_imei,
        mat_khau_may=d.mat_khau_may,
        ngay_tao=d.ngay_tao,
        ten_khach_hang=d.khach_hang.ho_ten if d.khach_hang else "N/A",
        so_dien_thoai_khach=d.khach_hang.so_dien_thoai if d.khach_hang else "N/A"
    )
