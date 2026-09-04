from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.db.models import NguoiDung
from backend.app.core.security import get_password_hash, require_roles, get_current_user
from backend.app.schemas.schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Quản lý Người dùng / Nhân sự (RBAC)"])

@router.get("", response_model=List[UserOut])
def list_users(
    vai_tro: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan"]))
):
    """Lấy danh sách người dùng / nhân viên trong hệ thống (Lọc theo vai trò nếu cần)."""
    query = db.query(NguoiDung)
    if vai_tro:
        query = query.filter(NguoiDung.vai_tro == vai_tro)
    return query.order_by(NguoiDung.id.asc()).all()

@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Lấy thông tin chi tiết một nhân viên (Chỉ Quản Lý)."""
    user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    return user

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    req: UserCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Thêm mới tài khoản nhân viên (Chỉ Quản Lý)."""
    existing = db.query(NguoiDung).filter(NguoiDung.ten_dang_nhap == req.ten_dang_nhap).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại trên hệ thống.")
    
    valid_roles = ["QuanLy", "LeTan", "KyThuatVien", "ThuNgan"]
    if req.vai_tro not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Vai trò không hợp lệ. Phải là một trong: {valid_roles}")

    new_user = NguoiDung(
        ten_dang_nhap=req.ten_dang_nhap.strip(),
        mat_khau_hash=get_password_hash(req.mat_khau),
        ho_ten=req.ho_ten.strip(),
        vai_tro=req.vai_tro,
        so_dien_thoai=req.so_dien_thoai.strip() if req.so_dien_thoai else None,
        trang_thai=req.trang_thai or "HoatDong"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    req: UserUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Cập nhật thông tin / phân quyền / trạng thái tài khoản nhân viên (Chỉ Quản Lý)."""
    user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    if req.ho_ten is not None:
        user.ho_ten = req.ho_ten.strip()
    if req.vai_tro is not None:
        valid_roles = ["QuanLy", "LeTan", "KyThuatVien", "ThuNgan"]
        if req.vai_tro not in valid_roles:
            raise HTTPException(status_code=400, detail=f"Vai trò không hợp lệ. Phải là một trong: {valid_roles}")
        user.vai_tro = req.vai_tro
    if req.so_dien_thoai is not None:
        user.so_dien_thoai = req.so_dien_thoai.strip()
    if req.trang_thai is not None:
        user.trang_thai = req.trang_thai
    if req.mat_khau:
        user.mat_khau_hash = get_password_hash(req.mat_khau)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Xóa hoặc vô hiệu hóa tài khoản nhân viên (Chỉ Quản Lý)."""
    user = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Không thể tự xóa tài khoản của chính mình.")

    db.delete(user)
    db.commit()
    return {"success": True, "message": f"Đã xóa tài khoản {user.ten_dang_nhap}."}
