import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hệ thống Quản lý Trung tâm Sửa chữa Điện thoại AI"
    VERSION: str = "2.1.0"
    API_V1_STR: str = "/api"
    
    # CSDL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./phone_repair.db")
    
    # Bảo mật JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "phone_repair_super_secret_jwt_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 giờ
    
    # Google Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
    AI_TIMEOUT_SECONDS: float = float(os.getenv("AI_TIMEOUT_SECONDS", "5.0"))

settings = Settings()

