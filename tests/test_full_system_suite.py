"""
Phân hệ Kiểm Thử Tích Hợp Toàn Trình (End-to-End System Integration Test)
PhoneCare AI - Kịch bản liên thông xuyên suốt các vai trò & phân hệ:
1. Hành trình sửa chữa: Tiếp nhận -> AI phân tích -> KTV sửa & xuất kho -> Thu ngân lập HĐ -> Bảo hành điện tử -> Tra cứu công khai.
2. Tra cứu tri thức doanh nghiệp: Truy vấn tài liệu RAG -> Trích xuất Top-K -> Sinh câu trả lời kèm trích dẫn.
3. Giám sát & An toàn: Thống kê Dashboard -> Kiểm toán AI Logs -> Sao lưu CSDL tự động (NFR-08).
"""

import sys
import os
import time
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.main import app
from backend.app.db.init_db import init_db
import backup_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Khởi tạo CSDL SQLite và nạp dữ liệu mẫu chuẩn trước khi chạy kiểm thử."""
    init_db()

def get_auth_header(username: str) -> dict:
    """Hàm tiện ích lấy JWT Token theo vai trò tài khoản."""
    res = client.post("/api/auth/login", json={"ten_dang_nhap": username, "mat_khau": "123456"})
    assert res.status_code == 200, f"Đăng nhập thất bại: {username}"
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


# =========================================================================
# KỊCH BẢN 1: HÀNH TRÌNH TIẾP NHẬN - SỬA CHỮA - THANH TOÁN - BẢO HÀNH (E2E)
# =========================================================================
def test_e2e_repair_and_warranty_journey():
    """Kiểm tra luồng liên thông giữa 4 vai trò: Lễ tân -> Trợ lý AI -> Kỹ thuật viên -> Thu ngân -> Khách hàng."""
    letan_hdr = get_auth_header("letan")
    ktv_hdr = get_auth_header("ktv")
    thungan_hdr = get_auth_header("thungan")
    ts = int(time.time() * 1000)
    phone = f"09{ts % 100000000:08d}"
    imei = f"35{ts}777"[:15]

    # Bước 1: Lễ tân tiếp nhận thiết bị mới từ khách hàng
    res_intake = client.post("/api/repairs", headers=letan_hdr, json={
        "ho_ten": "Nguyễn Văn Toàn",
        "so_dien_thoai": phone,
        "dia_chi": "Hà Nội",
        "hang_san_xuat": "Samsung",
        "model_may": "Galaxy S24 Ultra",
        "so_imei": imei,
        "mo_ta_loi_khach": "Rơi vỡ màn hình, sạc chập chờn nóng máy"
    })
    assert res_intake.status_code == 201
    phieu_id = res_intake.json()["phieu_id"]
    ma_phieu = res_intake.json()["ma_phieu"]

    # Bước 2: AI tóm tắt lỗi thô & soạn tin nhắn thông báo (FR-10, FR-11)
    res_ai_sum = client.post("/api/ai/summarize-fault", headers=letan_hdr, json={
        "phieu_id": phieu_id,
        "model_may": "Galaxy S24 Ultra",
        "mo_ta_loi_khach": "Rơi vỡ màn hình, sạc chập chờn nóng máy",
        "ghi_chu_ky_thuat": "Vỡ phôi AMOLED, cáp chân sạc Type-C oxy hóa"
    })
    assert res_ai_sum.status_code == 200
    assert "data" in res_ai_sum.json()

    # Bước 3: KTV nhận máy, chuyển trạng thái & xuất kho linh kiện thay thế
    res_status = client.patch(f"/api/repairs/{phieu_id}/status", headers=ktv_hdr, json={
        "trang_thai": "DangSuaChua",
        "ghi_chu_ky_thuat": "Đã nhận máy, tiến hành thay cụm chân sạc và ép kính"
    })
    assert res_status.status_code == 200

    parts = client.get("/api/parts", headers=ktv_hdr).json()
    assert len(parts) > 0
    part_sample = parts[0]
    initial_stock = part_sample["so_luong_ton"]

    res_add_part = client.post(f"/api/repairs/{phieu_id}/items", headers=ktv_hdr, json={
        "linh_kien_id": part_sample["id"],
        "so_luong": 1
    })
    assert res_add_part.status_code == 201

    # Kiểm tra tồn kho đã tự động giảm 1
    updated_part = client.get(f"/api/parts/{part_sample['id']}", headers=ktv_hdr).json()
    assert updated_part["so_luong_ton"] == initial_stock - 1

    # Bước 4: KTV sửa xong -> Thu ngân lập hóa đơn thanh toán
    client.patch(f"/api/repairs/{phieu_id}/status", headers=ktv_hdr, json={"trang_thai": "DaSuaXong"})
    res_inv = client.post("/api/invoices", headers=thungan_hdr, json={
        "phieu_sua_chua_id": phieu_id,
        "phuong_thuc_tt": "ChuyenKhoan"
    })
    assert res_inv.status_code == 201
    assert res_inv.json()["trang_thai_tt"] == "DaThanhToan"

    # Bước 5: Khách hàng tra cứu công khai tiến độ và bảo hành điện tử (Không cần token)
    res_track = client.get(f"/api/repairs/lookup?q={ma_phieu}")
    assert res_track.status_code == 200 and len(res_track.json()) >= 1

    res_warranty = client.get(f"/api/warranties/lookup?imei_or_phone={imei}")
    assert res_warranty.status_code == 200 and len(res_warranty.json()) >= 1


# =========================================================================
# KỊCH BẢN 2: TRA CỨU TRI THỨC DOANH NGHIỆP QUA RAG PIPELINE
# =========================================================================
def test_e2e_rag_knowledge_pipeline():
    """Kiểm tra chu trình RAG: Tìm kiếm văn bản tri thức -> Trích xuất ngữ cảnh -> Sinh câu trả lời có trích dẫn."""
    query = "Quy định bảo hành và đổi trả linh kiện khi thay thế tại cửa hàng"

    # 1. Trích xuất Top-K Chunks có độ tương đồng Cosine cao nhất trước khi gọi LLM
    res_ret = client.post("/api/ai/rag/retrieve", json={
        "query": query,
        "top_k": 3,
        "chunk_size": 300,
        "chunk_overlap": 50,
        "file_type_filter": "ALL"
    })
    assert res_ret.status_code == 200
    ret_data = res_ret.json()
    assert len(ret_data["retrieved_chunks"]) >= 1
    assert ret_data["retrieved_chunks"][0]["rank"] == 1

    # 2. Sinh câu trả lời có trích dẫn nguồn văn bản (Grounded Answer & Citations)
    res_gen = client.post("/api/ai/rag/generate", json={
        "query": query,
        "top_k": 3,
        "chunk_size": 300,
        "chunk_overlap": 50,
        "file_type_filter": "ALL"
    })
    assert res_gen.status_code == 200
    gen_data = res_gen.json()
    assert "answer" in gen_data and len(gen_data["answer"]) > 20
    assert "citations" in gen_data and len(gen_data["citations"]) >= 1


# =========================================================================
# KỊCH BẢN 3: GIÁM SÁT HỆ THỐNG, AUDIT LOG VÀ SAO LƯU CSDL (NFR-08)
# =========================================================================
def test_e2e_system_health_audit_and_backup():
    """Kiểm tra Dashboard giám sát thời gian thực, nhật ký AI Logs và tự động backup dữ liệu."""
    admin_hdr = get_auth_header("admin")

    # 1. Dashboard giám sát thời gian thực
    res_stats = client.get("/api/stats/overview", headers=admin_hdr)
    assert res_stats.status_code == 200
    assert res_stats.json()["status"] == "Healthy"

    # 2. Kiểm toán lịch sử AI (AI Audit Logs)
    res_logs = client.get("/api/ai/logs", headers=admin_hdr)
    assert res_logs.status_code == 200 and isinstance(res_logs.json(), list)

    # 3. Cơ chế sao lưu CSDL tự động định kỳ theo NFR-08
    backup_file = backup_db.create_backup()
    assert os.path.exists(backup_file) and os.path.getsize(backup_file) > 0
    if os.path.exists(backup_file):
        os.remove(backup_file)
