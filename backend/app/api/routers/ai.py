from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import PhieuSuaChua, NhatKyAI, NguoiDung
from backend.app.services.ai_service import GeminiAIService
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import (
    FaultSummaryRequest, ProgressMessageRequest, ServiceExplainRequest, ApproveAIDataRequest
)

router = APIRouter(prefix="/ai", tags=["Phân hệ Trợ lý AI (AI Orchestrator)"])

@router.post("/summarize-fault")
def ai_summarize_fault(
    req: FaultSummaryRequest,
    current_user: NguoiDung = Depends(get_current_user)
):
    """FR-10: KTV nhập ghi chú thô, AI tóm tắt thành JSON chuẩn hóa 4 trường."""
    res = GeminiAIService.summarize_fault(
        model_may=req.model_may,
        mo_ta_loi_khach=req.mo_ta_loi_khach,
        ghi_chu_ky_thuat=req.ghi_chu_ky_thuat,
        phieu_id=req.phieu_id
    )
    return res

@router.post("/generate-progress-message")
def ai_generate_progress_message(
    req: ProgressMessageRequest,
    current_user: NguoiDung = Depends(get_current_user)
):
    """FR-11: Lễ tân chọn thông tin phiếu, AI sinh tin nhắn SMS/Zalo lịch sự cho khách."""
    res = GeminiAIService.generate_progress_message(
        ten_khach=req.ten_khach,
        model_may=req.model_may,
        trang_thai=req.trang_thai,
        chi_phi=req.chi_phi,
        ngay_hen=req.ngay_hen,
        kenh_gui=req.kenh_gui,
        phieu_id=req.phieu_id
    )
    return res

@router.post("/explain-service")
def ai_explain_service(
    req: ServiceExplainRequest,
    current_user: NguoiDung = Depends(get_current_user)
):
    """FR-12: AI diễn giải bằng ngôn ngữ đời thường (metaphor) lý do hỏng hóc và tại sao cần sửa/thay."""
    res = GeminiAIService.explain_service(
        ten_dich_vu=req.ten_dich_vu,
        ten_linh_kien=req.ten_linh_kien,
        loi_thuc_te=req.loi_thuc_te,
        phieu_id=req.phieu_id
    )
    return res

@router.post("/approve-and-save")
def approve_ai_data(
    req: ApproveAIDataRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "KyThuatVien", "LeTan"]))
):
    """Human-in-the-loop: Phê duyệt bản nháp đề xuất từ AI để lưu chính thức vào CSDL."""
    phieu = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == req.phieu_id).first()
    if not phieu:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")
    
    if req.ai_tom_tat_loi is not None:
        phieu.ai_tom_tat_loi = req.ai_tom_tat_loi
    if req.ai_giai_thich_dv is not None:
        phieu.ai_giai_thich_dv = req.ai_giai_thich_dv
    if req.ghi_chu_ky_thuat is not None:
        phieu.ghi_chu_ky_thuat = req.ghi_chu_ky_thuat
    if req.trang_thai_moi is not None:
        phieu.trang_thai = req.trang_thai_moi

    db.commit()
    db.refresh(phieu)
    return {
        "success": True,
        "message": "Đã phê duyệt và lưu dữ liệu AI chính thức vào CSDL!",
        "phieu_id": phieu.id,
        "ma_phieu": phieu.ma_phieu,
        "trang_thai": phieu.trang_thai
    }

@router.get("/logs")
def list_ai_logs(
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách Audit Logs lịch sử gọi AI để phục vụ đánh giá và truy vết."""
    logs = db.query(NhatKyAI).order_by(NhatKyAI.id.desc()).limit(50).all()
    result = []
    for l in logs:
        result.append({
            "id": l.id,
            "phieu_id": l.phieu_sua_chua_id,
            "loai_tac_vu": l.loai_tac_vu,
            "model": l.model_name,
            "exec_time_ms": l.execution_time_ms,
            "trang_thai": l.trang_thai,
            "ngay_thuc_hien": l.ngay_thuc_hien.strftime("%d/%m/%Y %H:%M:%S") if l.ngay_thuc_hien else None,
            "prompt_input": l.prompt_input,
            "ai_raw_response": l.ai_raw_response,
            "parsed_json": l.ai_parsed_json
        })
    return result


@router.get("/benchmark/cases")
def list_benchmark_cases(current_user: NguoiDung = Depends(get_current_user)):
    """Lấy danh sách 20 ca bệnh phần cứng thực tế trong bộ Benchmark Dataset."""
    from backend.app.services.ai_benchmark import AIBenchmarkEngine
    return AIBenchmarkEngine.get_all_cases()


@router.get("/benchmark/summary")
def get_benchmark_summary(current_user: NguoiDung = Depends(get_current_user)):
    """Lấy bảng tổng hợp kết quả đo lường 5 chỉ số kỹ thuật của 3 kỹ thuật Prompting."""
    from backend.app.services.ai_benchmark import AIBenchmarkEngine
    return AIBenchmarkEngine.get_summary()


@router.post("/benchmark/evaluate/{case_id}")
def evaluate_benchmark_case(case_id: int, current_user: NguoiDung = Depends(get_current_user)):
    """Chạy thử nghiệm A/B so sánh trực tiếp Zero-shot vs Few-shot vs CoT cho 1 ca bệnh."""
    from backend.app.services.ai_benchmark import AIBenchmarkEngine
    return AIBenchmarkEngine.evaluate_case_simulated(case_id)


@router.post("/benchmark/test-repair")
def test_json_repair(payload: dict, current_user: NguoiDung = Depends(get_current_user)):
    """Kiểm thử tính năng tự động sửa lỗi cấu trúc JSON (JSONRepairEngine)."""
    from backend.app.services.ai_service import JSONRepairEngine
    raw_text = payload.get("raw_text", "")
    repaired = JSONRepairEngine.repair_and_parse(raw_text)
    return {
        "success": repaired is not None,
        "input_text": raw_text,
        "repaired_data": repaired
    }


@router.post("/benchmark/test-injection")
def test_injection_defense(payload: dict, current_user: NguoiDung = Depends(get_current_user)):
    """Kiểm thử cơ chế phòng vệ chống Prompt Injection và bảo vệ PII (DataSanitizer)."""
    from backend.app.services.ai_service import DataSanitizer
    text = payload.get("text", "")
    sanitized = DataSanitizer.sanitize(text)
    return {
        "original": text,
        "sanitized": sanitized,
        "blocked_injection": "[BLOCKED_INJECTION]" in sanitized,
        "redacted_pii": any(tag in sanitized for tag in ["[REDACTED_PHONE]", "[REDACTED_EMAIL]", "[REDACTED_PASS]"])
    }

