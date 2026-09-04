from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.db.models import KhachHang, NguoiDung
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import CustomerCreate, CustomerUpdate, CustomerOut

router = APIRouter(prefix="/customers", tags=["Quản lý Khách hàng"])

@router.get("", response_model=List[CustomerOut])
def list_customers(
    q: Optional[str] = Query(None, description="Tìm kiếm theo Tên hoặc Số điện thoại"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách khách hàng, hỗ trợ tìm kiếm theo số điện thoại hoặc tên."""
    query = db.query(KhachHang)
    if q:
        search = f"%{q.strip()}%"
        query = query.filter((KhachHang.ho_ten.ilike(search)) | (KhachHang.so_dien_thoai.ilike(search)))
    
    customers = query.order_by(KhachHang.id.desc()).offset(skip).limit(limit).all()
    
    result = []
    for c in customers:
        result.append(CustomerOut(
            id=c.id,
            ho_ten=c.ho_ten,
            so_dien_thoai=c.so_dien_thoai,
            dia_chi=c.dia_chi,
            ngay_tao=c.ngay_tao,
            so_thiet_bi=len(c.thiet_bi),
            so_phieu_sua=len(c.phieu_sua_chua)
        ))
    return result

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xem thông tin chi tiết một khách hàng."""
    c = db.query(KhachHang).filter(KhachHang.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng.")
    return CustomerOut(
        id=c.id,
        ho_ten=c.ho_ten,
        so_dien_thoai=c.so_dien_thoai,
        dia_chi=c.dia_chi,
        ngay_tao=c.ngay_tao,
        so_thiet_bi=len(c.thiet_bi),
        so_phieu_sua=len(c.phieu_sua_chua)
    )

@router.post("", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(
    req: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan"]))
):
    """Tạo hồ sơ khách hàng mới."""
    existing = db.query(KhachHang).filter(KhachHang.so_dien_thoai == req.so_dien_thoai.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Số điện thoại này đã được đăng ký trong hệ thống.")
    
    c = KhachHang(
        ho_ten=req.ho_ten.strip(),
        so_dien_thoai=req.so_dien_thoai.strip(),
        dia_chi=req.dia_chi.strip() if req.dia_chi else None
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return CustomerOut(
        id=c.id,
        ho_ten=c.ho_ten,
        so_dien_thoai=c.so_dien_thoai,
        dia_chi=c.dia_chi,
        ngay_tao=c.ngay_tao,
        so_thiet_bi=0,
        so_phieu_sua=0
    )

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(
    customer_id: int,
    req: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan"]))
):
    """Cập nhật thông tin khách hàng."""
    c = db.query(KhachHang).filter(KhachHang.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng.")
    
    if req.so_dien_thoai and req.so_dien_thoai.strip() != c.so_dien_thoai:
        existing = db.query(KhachHang).filter(KhachHang.so_dien_thoai == req.so_dien_thoai.strip()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Số điện thoại đã thuộc về khách hàng khác.")
        c.so_dien_thoai = req.so_dien_thoai.strip()
    
    if req.ho_ten is not None:
        c.ho_ten = req.ho_ten.strip()
    if req.dia_chi is not None:
        c.dia_chi = req.dia_chi.strip()
    
    db.commit()
    db.refresh(c)
    return CustomerOut(
        id=c.id,
        ho_ten=c.ho_ten,
        so_dien_thoai=c.so_dien_thoai,
        dia_chi=c.dia_chi,
        ngay_tao=c.ngay_tao,
        so_thiet_bi=len(c.thiet_bi),
        so_phieu_sua=len(c.phieu_sua_chua)
    )

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Xóa hồ sơ khách hàng (Chỉ Quản Lý)."""
    c = db.query(KhachHang).filter(KhachHang.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng.")
    
    if len(c.phieu_sua_chua) > 0:
        raise HTTPException(status_code=400, detail="Không thể xóa khách hàng đã có lịch sử sửa chữa.")
    
    db.delete(c)
    db.commit()
    return {"success": True, "message": f"Đã xóa khách hàng {c.ho_ten} thành công."}
