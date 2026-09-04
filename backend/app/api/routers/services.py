from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.db.models import DichVu, NguoiDung
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import ServiceCreate, ServiceUpdate, ServiceOut

router = APIRouter(prefix="/services", tags=["Quản lý Dịch vụ Kỹ thuật & Bảng giá"])

@router.get("", response_model=List[ServiceOut])
def list_services(
    q: Optional[str] = Query(None, description="Tìm kiếm theo Tên hoặc Mã dịch vụ"),
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh mục các dịch vụ sửa chữa và bảng giá công."""
    query = db.query(DichVu)
    if q:
        search = f"%{q.strip()}%"
        query = query.filter((DichVu.ten_dich_vu.ilike(search)) | (DichVu.ma_dich_vu.ilike(search)))
    return query.order_by(DichVu.id.asc()).all()

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xem chi tiết một dịch vụ kỹ thuật."""
    s = db.query(DichVu).filter(DichVu.id == service_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ.")
    return s

@router.post("", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(
    req: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Thêm dịch vụ kỹ thuật mới (Chỉ Quản Lý)."""
    existing = db.query(DichVu).filter(DichVu.ma_dich_vu == req.ma_dich_vu.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã dịch vụ đã tồn tại.")

    s = DichVu(
        ma_dich_vu=req.ma_dich_vu.strip(),
        ten_dich_vu=req.ten_dich_vu.strip(),
        gia_cong=req.gia_cong,
        mo_ta=req.mo_ta.strip() if req.mo_ta else None
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    req: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Cập nhật thông tin dịch vụ / giá công (Chỉ Quản Lý)."""
    s = db.query(DichVu).filter(DichVu.id == service_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ.")

    if req.ma_dich_vu and req.ma_dich_vu.strip() != s.ma_dich_vu:
        existing = db.query(DichVu).filter(DichVu.ma_dich_vu == req.ma_dich_vu.strip()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Mã dịch vụ bị trùng.")
        s.ma_dich_vu = req.ma_dich_vu.strip()

    if req.ten_dich_vu is not None:
        s.ten_dich_vu = req.ten_dich_vu.strip()
    if req.gia_cong is not None:
        s.gia_cong = req.gia_cong
    if req.mo_ta is not None:
        s.mo_ta = req.mo_ta.strip()

    db.commit()
    db.refresh(s)
    return s

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Xóa dịch vụ kỹ thuật (Chỉ Quản Lý)."""
    s = db.query(DichVu).filter(DichVu.id == service_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ.")

    db.delete(s)
    db.commit()
    return {"success": True, "message": f"Đã xóa dịch vụ {s.ten_dich_vu} thành công."}
