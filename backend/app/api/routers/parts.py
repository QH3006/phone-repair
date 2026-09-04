from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.db.models import LinhKien, NguoiDung
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import PartCreate, PartUpdate, PartOut

router = APIRouter(prefix="/parts", tags=["Quản lý Kho Linh Kiện"])

@router.get("", response_model=List[PartOut])
def list_parts(
    q: Optional[str] = Query(None, description="Tìm kiếm theo Tên hoặc Mã linh kiện"),
    low_stock: Optional[bool] = Query(False, description="Chỉ hiện linh kiện sắp hết (tồn kho <= 5)"),
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách linh kiện trong kho, có cảnh báo tồn kho thấp."""
    query = db.query(LinhKien)
    if q:
        search = f"%{q.strip()}%"
        query = query.filter((LinhKien.ten_linh_kien.ilike(search)) | (LinhKien.ma_linh_kien.ilike(search)) | (LinhKien.loai_may.ilike(search)))
    if low_stock:
        query = query.filter(LinhKien.so_luong_ton <= 5)
    
    return query.order_by(LinhKien.id.desc()).all()

@router.get("/{part_id}", response_model=PartOut)
def get_part(
    part_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xem thông tin chi tiết một linh kiện."""
    p = db.query(LinhKien).filter(LinhKien.id == part_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy linh kiện.")
    return p

@router.post("", response_model=PartOut, status_code=status.HTTP_201_CREATED)
def create_part(
    req: PartCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "KyThuatVien"]))
):
    """Thêm mới linh kiện vào kho."""
    existing = db.query(LinhKien).filter(LinhKien.ma_linh_kien == req.ma_linh_kien.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã linh kiện đã tồn tại.")

    p = LinhKien(
        ma_linh_kien=req.ma_linh_kien.strip(),
        ten_linh_kien=req.ten_linh_kien.strip(),
        loai_may=req.loai_may.strip() if req.loai_may else None,
        gia_nhap=req.gia_nhap,
        gia_ban=req.gia_ban,
        so_luong_ton=req.so_luong_ton,
        thoi_han_bao_hanh_thang=req.thoi_han_bao_hanh_thang
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/{part_id}", response_model=PartOut)
def update_part(
    part_id: int,
    req: PartUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "KyThuatVien"]))
):
    """Cập nhật thông tin linh kiện / số lượng tồn kho / giá bán."""
    p = db.query(LinhKien).filter(LinhKien.id == part_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy linh kiện.")

    if req.ma_linh_kien and req.ma_linh_kien.strip() != p.ma_linh_kien:
        existing = db.query(LinhKien).filter(LinhKien.ma_linh_kien == req.ma_linh_kien.strip()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Mã linh kiện bị trùng.")
        p.ma_linh_kien = req.ma_linh_kien.strip()

    if req.ten_linh_kien is not None:
        p.ten_linh_kien = req.ten_linh_kien.strip()
    if req.loai_may is not None:
        p.loai_may = req.loai_may.strip()
    if req.gia_nhap is not None:
        p.gia_nhap = req.gia_nhap
    if req.gia_ban is not None:
        p.gia_ban = req.gia_ban
    if req.so_luong_ton is not None:
        p.so_luong_ton = req.so_luong_ton
    if req.thoi_han_bao_hanh_thang is not None:
        p.thoi_han_bao_hanh_thang = req.thoi_han_bao_hanh_thang

    db.commit()
    db.refresh(p)
    return p

@router.delete("/{part_id}")
def delete_part(
    part_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Xóa linh kiện khỏi kho (Chỉ Quản Lý)."""
    p = db.query(LinhKien).filter(LinhKien.id == part_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy linh kiện.")
    
    db.delete(p)
    db.commit()
    return {"success": True, "message": f"Đã xóa linh kiện {p.ten_linh_kien} thành công."}
