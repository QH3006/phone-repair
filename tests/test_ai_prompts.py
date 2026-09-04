import sys
import os
import pytest
import json

# Đảm bảo đường dẫn gốc của dự án luôn nằm trong sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.services.ai_service import DataSanitizer, PromptTemplates, GeminiAIService
from backend.app.db.database import SessionLocal, Base, engine

from backend.app.db.models import NguoiDung, PhieuSuaChua, LinhKien, KhachHang, ThietBi
from backend.app.db.init_db import init_db

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Khởi tạo database trước khi chạy test."""
    init_db()

def test_data_sanitizer():
    """Kiểm tra lớp lọc và làm sạch thông tin cá nhân (PII Data Sanitization)."""
    raw_text = "Khách hàng tên Minh, SĐT 0988123456, địa chỉ Cầu Giấy, mật khẩu: 123456, email minh@gmail.com"
    clean = DataSanitizer.sanitize(raw_text)
    
    assert "0988123456" not in clean
    assert "[REDACTED_PHONE]" in clean
    assert "[REDACTED_EMAIL]" in clean
    assert "[REDACTED_PASS]" in clean

def test_prompt_template_structure_5_components():
    """Kiểm tra bộ Prompt có đầy đủ 5 thành phần theo chuẩn Chương 3."""
    prompt = PromptTemplates.get_fault_summary_prompt(
        model_may="iPhone 13 Pro Max",
        mo_ta_loi_khach="Máy sập nguồn",
        ghi_chu_ky_thuat="Chập tụ C2301"
    )
    
    assert "[Instructions]" in prompt
    assert "[Context]" in prompt
    assert "[Constraints]" in prompt
    assert "[Examples]" in prompt
    assert "[Output Format]" in prompt
    assert "iPhone 13 Pro Max" in prompt

def test_fault_summary_service():
    """Kiểm tra dịch vụ AI Tóm tắt lỗi (FR-10) trả về đúng 4 trường schema."""
    res = GeminiAIService.summarize_fault(
        model_may="iPhone 13 Pro Max",
        mo_ta_loi_khach="Máy ngâm nước mất nguồn",
        ghi_chu_ky_thuat="Chập đường VDD_MAIN do tụ C2301 rỉ sét. IC sạc USB U3300 nóng."
    )
    
    assert res["status"] in ["ThanhCong", "Fallback"]
    assert "data" in res
    data = res["data"]
    assert "hardware_issue" in data
    assert "faulty_components" in data
    assert "recommended_action" in data
    assert "risk_level" in data
    assert data["risk_level"] in ["Thap", "TrungBinh", "Cao"]

def test_progress_message_service():
    """Kiểm tra dịch vụ AI Sinh tin nhắn tiến độ (FR-11)."""
    res = GeminiAIService.generate_progress_message(
        ten_khach="Anh Minh",
        model_may="Galaxy S22 Ultra",
        trang_thai="DaSuaXong",
        chi_phi=850000,
        ngay_hen="Trước 18h",
        kenh_gui="SMS"
    )
    assert res["status"] in ["ThanhCong", "Fallback"]
    assert "message" in res["data"]
    assert len(res["data"]["message"]) > 10

def test_service_explanation():
    """Kiểm tra dịch vụ AI Diễn giải dịch vụ (FR-12)."""
    res = GeminiAIService.explain_service(
        ten_dich_vu="Thay IC Hiển thị",
        ten_linh_kien="IC Display U2",
        loi_thuc_te="Màn hình tối đen"
    )
    assert res["status"] in ["ThanhCong", "Fallback"]
    assert "message" in res["data"]
    assert len(res["data"]["message"]) > 20

def test_database_seed_integrity():
    """Kiểm tra tính toàn vẹn của CSDL và dữ liệu mẫu (Seed data)."""
    db = SessionLocal()
    try:
        users = db.query(NguoiDung).all()
        assert len(users) >= 4
        roles = [u.vai_tro for u in users]
        assert "QuanLy" in roles
        assert "LeTan" in roles
        assert "KyThuatVien" in roles
        assert "ThuNgan" in roles

        repairs = db.query(PhieuSuaChua).all()
        assert len(repairs) >= 3
    finally:
        db.close()
