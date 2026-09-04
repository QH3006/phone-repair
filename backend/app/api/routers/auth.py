from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import NguoiDung
from backend.app.core.security import verify_password, get_password_hash, create_access_token, get_current_user
from backend.app.schemas.schemas import LoginRequest, LoginResponse, ChangePasswordRequest, UserOut

router = APIRouter(prefix="/auth", tags=["Xác thực & Tài khoản (Auth & RBAC)"])

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Đăng nhập hệ thống, kiểm tra mật khẩu băm và cấp JWT token kèm vai trò (RBAC)."""
    user = db.query(NguoiDung).filter(NguoiDung.ten_dang_nhap == req.ten_dang_nhap).first()
    if not user or not verify_password(req.mat_khau, user.mat_khau_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác."
        )
    if user.trang_thai != "HoatDong":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị tạm khóa bởi Quản trị viên."
        )
    
    token = create_access_token(subject=user.id, role=user.vai_tro)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        id=user.id,
        ho_ten=user.ho_ten,
        vai_tro=user.vai_tro,
        ten_dang_nhap=user.ten_dang_nhap,
        so_dien_thoai=user.so_dien_thoai
    )

@router.get("/me", response_model=UserOut)
def get_me(current_user: NguoiDung = Depends(get_current_user)):
    """Lấy thông tin tài khoản của người dùng đang đăng nhập."""
    return current_user

@router.post("/change-password")
def change_password(
    req: ChangePasswordRequest,
    current_user: NguoiDung = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Đổi mật khẩu cho người dùng hiện tại."""
    if not verify_password(req.mat_khau_cu, current_user.mat_khau_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu cũ không chính xác."
        )
    
    current_user.mat_khau_hash = get_password_hash(req.mat_khau_moi)
    db.commit()
    return {"success": True, "message": "Đổi mật khẩu thành công!"}
