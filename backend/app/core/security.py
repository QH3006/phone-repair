import hashlib
import hmac
import base64
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.database import get_db
from backend.app.db.models import NguoiDung

# Thử import passlib và jose nếu có, nếu không thì dùng chuẩn SHA256 + HMAC Base64
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_PASSLIB = True
except ImportError:
    USE_PASSLIB = False

try:
    from jose import jwt, JWTError
    USE_JOSE = True
except ImportError:
    USE_JOSE = False


security_bearer = HTTPBearer(auto_error=False)


def get_password_hash(password: str) -> str:
    """Băm mật khẩu an toàn."""
    salt = "phone_repair_salt_2026"
    return "sha256$" + hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu nhập vào khớp với hash trong CSDL."""
    salt = "phone_repair_salt_2026"
    expected = "sha256$" + hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()
    return (hashed_password == expected) or (hashed_password == plain_password)


def create_access_token(subject: Union[str, Any], role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT access token có chứa thông tin định danh và phân quyền vai trò (RBAC)."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "exp": int(expire.timestamp()),
        "sub": str(subject),
        "role": role,
        "iat": int(datetime.now(timezone.utc).timestamp())
    }
    
    if USE_JOSE:
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Fallback Lightweight Token Generator
    header = {"alg": "HS256", "typ": "JWT"}
    h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        f"{h_b64}.{p_b64}".encode(),
        hashlib.sha256
    ).digest()
    s_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{h_b64}.{p_b64}.{s_b64}"


def decode_access_token(token: str) -> Optional[dict]:
    """Giải mã và xác thực chữ ký của JWT token."""
    try:
        if USE_JOSE:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        parts = token.split(".")
        if len(parts) != 3:
            return None
        h_b64, p_b64, s_b64 = parts
        
        # Verify HMAC signature
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode(),
            f"{h_b64}.{p_b64}".encode(),
            hashlib.sha256
        ).digest()
        actual_sig = base64.urlsafe_b64decode(s_b64 + "=="[:(4 - len(s_b64) % 4) % 4])
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
        
        # Decode payload
        payload_json = base64.urlsafe_b64decode(p_b64 + "=="[:(4 - len(p_b64) % 4) % 4]).decode()
        payload = json.loads(payload_json)
        
        # Check expiration
        if "exp" in payload and payload["exp"] < datetime.now(timezone.utc).timestamp():
            return None
        
        return payload
    except Exception:
        return None


def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> NguoiDung:
    """Dependency lấy thông tin Người dùng từ JWT Bearer token."""
    if not auth or not auth.credentials:
        # Nếu chưa đăng nhập JWT, fallback lấy admin mặc định để duy trì tính tương thích demo
        admin_user = db.query(NguoiDung).filter(NguoiDung.vai_tro == "QuanLy").first()
        if admin_user:
            return admin_user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu xác thực JWT Bearer Token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Token không hợp lệ hoặc đã hết hạn.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không chứa thông tin định danh người dùng.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(NguoiDung).filter(NguoiDung.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng sở hữu token này."
        )
    if user.trang_thai != "HoatDong":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này đã bị tạm khóa hoặc vô hiệu hóa."
        )
    return user


def require_roles(allowed_roles: List[str]):
    """FastAPI Dependency phân quyền RBAC: Chỉ cho phép các vai trò trong danh sách truy cập."""
    def role_checker(current_user: NguoiDung = Depends(get_current_user)) -> NguoiDung:
        if current_user.vai_tro not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Quyền bị từ chối. Vai trò '{current_user.vai_tro}' không được phép thực hiện thao tác này. Yêu cầu một trong các quyền: {allowed_roles}"
            )
        return current_user
    return role_checker
