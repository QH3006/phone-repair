import re
import json
import time
from typing import Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.db.database import SessionLocal
from backend.app.db.models import NhatKyAI

class DataSanitizer:
    """Lớp làm sạch và ẩn danh hóa dữ liệu (PII Data Sanitization) trước khi gửi qua Cloud LLM."""
    
    @staticmethod
    def sanitize(text: str) -> str:
        if not text:
            return ""
        # 1. Ẩn số điện thoại Việt Nam (10-11 số)
        sanitized = re.sub(r'(\b0|\+84)[3|5|7|8|9][0-9]{8}\b', '[REDACTED_PHONE]', text)
        # 2. Ẩn mật khẩu máy được ghi trong text
        sanitized = re.sub(r'(pass|mật khẩu|passcode|pin):\s*[^\s,]+', r'\1: [REDACTED_PASS]', sanitized, flags=re.IGNORECASE)
        # 3. Ẩn email
        sanitized = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', sanitized)
        # 4. Loại bỏ các từ khóa tấn công Prompt Injection tiềm ẩn
        sanitized = re.sub(r'(ignore previous instructions|system prompt|override system)', '[BLOCKED_INJECTION]', sanitized, flags=re.IGNORECASE)
        return sanitized


class PromptTemplates:
    """Quản lý các bộ Prompt chuẩn 5 thành phần theo giáo trình Chương 3."""

    @staticmethod
    def get_fault_summary_prompt(model_may: str, mo_ta_loi_khach: str, ghi_chu_ky_thuat: str) -> str:
        """Prompt 1: AI Tóm tắt tình trạng máy từ ghi chú KTV (FR-10)."""
        prompt = f"""[Instructions]
Bạn là chuyên gia phân tích kỹ thuật phần cứng điện thoại tại trung tâm bảo hành sửa chữa. Nhiệm vụ của bạn là đọc ghi chú kỹ thuật thô của KTV và chuyển đổi thành cấu trúc dữ liệu chuẩn hóa JSON.

[Context]
Hệ thống quản lý trung tâm sửa chữa điện thoại PhoneCare. Báo cáo này sẽ được Lễ tân và Quản lý sử dụng để lập bảng báo giá và xuất linh kiện.

[Constraints]
1. Tuyệt đối không tự suy diễn hoặc bịa đặt các lỗi không được đề cập trong ghi chú kỹ thuật.
2. Trả về đúng 1 khối JSON hợp lệ duy nhất, không kèm câu chào hay văn bản giải thích ngoài khối JSON.
3. Ràng buộc trường: "risk_level" chỉ được nhận 1 trong 3 giá trị: "Thap", "TrungBinh", "Cao".
4. Schema JSON bắt buộc có đủ 4 trường: "hardware_issue", "faulty_components", "recommended_action", "risk_level".

[Examples]
Input:
Model: iPhone 12 Pro Max
Ghi chú KTV: "Máy rơi nước, mất nguồn. Đo đường VDD_MAIN thấy chạm chập do tụ C2301 rỉ sét. IC sạc USB U3300 nóng bất thường. Pin sưng nhẹ 75%."
Output:
{{
  "hardware_issue": "Máy ngấm nước gây chập nguồn đường VDD_MAIN và hỏng IC sạc USB, pin bị phù nhẹ",
  "faulty_components": ["Tụ C2301", "IC sạc USB U3300", "Pin"],
  "recommended_action": "Thay thế tụ C2301, thay mới IC sạc USB, thay pin mới",
  "risk_level": "Cao"
}}

[Input Data]
Model máy: {model_may}
Mô tả lỗi từ khách hàng: {mo_ta_loi_khach}
Ghi chú kỹ thuật của KTV: {ghi_chu_ky_thuat}

[Output Format]
Chỉ trả về duy nhất khối JSON theo schema đã chỉ định.
"""
        return prompt

    @staticmethod
    def get_progress_message_prompt(ten_khach: str, model_may: str, trang_thai: str, chi_phi: float, ngay_hen: str, kenh_gui: str = "SMS") -> str:
        """Prompt 2: AI Sinh tin nhắn cập nhật tiến độ (FR-11)."""
        prompt = f"""[Instructions]
Bạn là nhân viên chăm sóc khách hàng chuyên nghiệp của Trung tâm sửa chữa điện thoại PhoneCare. Nhiệm vụ của bạn là soạn tin nhắn cập nhật tiến độ sửa máy cho khách hàng.

[Context]
Tin nhắn sẽ được gửi qua kênh {kenh_gui} của khách hàng. Giọng văn cần lịch sự, thân thiện, rõ ràng, minh bạch và tạo sự an tâm.

[Constraints]
1. Độ dài tin nhắn: Dưới 160 ký tự (nếu kênh là SMS) hoặc dưới 250 từ (nếu kênh là Zalo).
2. Phải nêu rõ: Tên khách hàng, dòng máy, trạng thái hiện tại, chi phí dự kiến (nếu có), thời gian hẹn dự kiến hoặc hotline hỗ trợ 1900.6868.
3. Không sử dụng thuật ngữ phần cứng phức tạp; không hứa hẹn điều chưa được xác nhận.

[Examples]
Input:
Khách hàng: Anh Minh | Model: Samsung S22 Ultra | Trạng thái: DaSuaXong | Chi phí: 850.000đ | Giờ hẹn: Trước 18h hôm nay | Kênh: SMS
Output:
"PhoneCare: Chào anh Minh, máy Samsung S22 Ultra đã sửa xong và kiểm tra hoàn tất. Tổng chi phí là 850.000đ. Kính mời anh ghé nhận máy trước 18h hôm nay. Hotline: 1900.6868."

[Input Data]
- Khách hàng: {ten_khach}
- Thiết bị: {model_may}
- Trạng thái tiến độ: {trang_thai}
- Chi phí dự kiến: {chi_phi:,.0f} VNĐ
- Thời gian hẹn: {ngay_hen}
- Kênh gửi: {kenh_gui}

[Output Format]
Chỉ trả về nội dung tin nhắn dạng chuỗi văn bản (Plain Text) hoàn chỉnh.
"""
        return prompt

    @staticmethod
    def get_service_explanation_prompt(ten_dich_vu: str, ten_linh_kien: str, loi_thuc_te: str) -> str:
        """Prompt 3: AI Diễn giải lỗi và dịch vụ sửa chữa cho khách hàng (FR-12)."""
        prompt = f"""[Instructions]
Bạn là chuyên viên tư vấn kỹ thuật am hiểu tâm lý khách hàng. Hãy giải thích nguyên nhân hỏng hóc và lý do cần thực hiện dịch vụ sửa chữa bằng ngôn ngữ đời thường, dễ hiểu, tránh dùng từ kỹ thuật hàn lâm.

[Context]
Khách hàng đang xem chi tiết báo giá sửa chữa trên cổng tra cứu trực tuyến và cần hiểu rõ vì sao linh kiện của họ bị hỏng và việc thay thế mang lại lợi ích gì.

[Constraints]
1. Bắt buộc sử dụng hình ảnh so sánh trực quan, dễ liên tưởng (metaphor đời sống).
2. Giải thích 3 ý chính: (1) Hiện tượng hỏng là gì? (2) Nguyên nhân do đâu? (3) Nếu không sửa thì ảnh hưởng thế nào?
3. Giọng văn chân thành, khách quan, trung thực, không mang tính ép buộc mua hàng.

[Examples]
Input:
Dịch vụ: "Thay IC Hiển Thị Màn Hình" | Lỗi: "Màn hình tối đen nhưng máy vẫn rung chuông khi có cuộc gọi".
Output:
"Điện thoại của bạn giống như một chiếc máy tính thu nhỏ, trong đó IC hiển thị đóng vai trò như một công tắc đèn chuyên cấp điện và tín hiệu cho màn hình. Khi công tắc này bị hỏng (thường do máy bị va đập hoặc ngấm ẩm), màn hình sẽ không thể sáng lên dù các bộ phận khác bên trong vẫn chạy bình thường. Việc thay thế IC hiển thị sẽ giúp màn hình sáng rõ trở lại như ban đầu mà không cần phải thay toàn bộ cụm màn hình đắt đỏ."

[Input Data]
Dịch vụ đề xuất: {ten_dich_vu}
Tên linh kiện: {ten_linh_kien}
Hiện tượng lỗi thực tế: {loi_thuc_te}

[Output Format]
Đoạn văn giải thích ngắn gọn từ 3 đến 5 câu.
"""
        return prompt


class GeminiAIService:
    """Service điều phối AI (AI Orchestrator) tích hợp Google Gemini API kèm cơ chế Fallback và Audit Logging."""

    @staticmethod
    def _call_gemini_or_fallback(prompt: str, task_type: str, fallback_data: Any) -> Dict[str, Any]:
        start_time = time.time()
        raw_text = ""
        parsed_data = None
        status = "ThanhCong"
        
        # Thử kết nối Google Gemini API nếu có cấu hình API KEY
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
                response = model.generate_content(prompt)
                raw_text = response.text
            except Exception as e:
                print(f"[AI Service Warning] Lỗi gọi Gemini API ({e}), chuyển sang chế độ Fallback.")
                status = "Fallback"
        else:
            status = "Fallback"

        # Nếu ở trạng thái Fallback (hoặc chưa có key), sinh phản hồi giả lập ngữ nghĩa chất lượng cao
        if status == "Fallback" or not raw_text:
            raw_text = GeminiAIService._generate_local_fallback(task_type, fallback_data)

        # Xử lý parse JSON nếu là tác vụ tóm tắt
        if task_type == "TomTatLoi":
            parsed_data = GeminiAIService._extract_json(raw_text)
            if not parsed_data:
                parsed_data = {
                    "hardware_issue": fallback_data.get("mo_ta_loi_khach", "Lỗi phần cứng chưa xác định"),
                    "faulty_components": ["Cần kiểm tra sâu"],
                    "recommended_action": "Kiểm tra và đo đạc lại bằng thiết bị chuyên dụng",
                    "risk_level": "TrungBinh"
                }
                status = "Fallback"
        elif task_type == "GiaiThichDichVu":
            parsed_data = {
                "message": raw_text.strip(),
                "explanation": raw_text.strip()
            }
        else:
            parsed_data = {"message": raw_text.strip()}

        exec_time_ms = round((time.time() - start_time) * 1000, 2)
        
        # Ghi nhật ký vào CSDL (NhatKyAI)
        GeminiAIService._log_ai_request(
            phieu_id=fallback_data.get("phieu_id"),
            task_type=task_type,
            prompt=prompt,
            raw_response=raw_text,
            parsed_json=json.dumps(parsed_data, ensure_ascii=False),
            exec_time_ms=exec_time_ms,
            status=status
        )

        return {
            "status": status,
            "execution_time_ms": exec_time_ms,
            "raw_response": raw_text,
            "data": parsed_data
        }

    @staticmethod
    def _extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Sử dụng Regex để trích xuất và sửa lỗi khối JSON từ văn bản phản hồi."""
        try:
            # Tìm khối giữa ```json và ``` hoặc giữa { và }
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            return None
        except Exception:
            return None

    @staticmethod
    def _generate_local_fallback(task_type: str, data: Dict[str, Any]) -> str:
        """Bộ sinh kết quả cục bộ phòng thủ (Rule-Based Semantic Fallback) khi mất mạng/hết quota."""
        if task_type == "TomTatLoi":
            model = data.get("model_may", "Điện thoại")
            notes = data.get("ghi_chu_ky_thuat", "")
            
            # Nhận diện từ khóa cơ bản
            comps = []
            if "pin" in notes.lower(): comps.append("Pin")
            if "màn" in notes.lower() or "cảm ứng" in notes.lower(): comps.append("Màn hình/Cảm ứng")
            if "nguồn" in notes.lower() or "u2" in notes.lower() or "vdd" in notes.lower(): comps.append("IC Nguồn/Mainboard")
            if "sạc" in notes.lower() or "chân sạc" in notes.lower(): comps.append("Cụm cáp sạc")
            if not comps: comps = ["Linh kiện phần cứng"]

            res = {
                "hardware_issue": f"Kiểm tra {model}: {notes[:100]}...",
                "faulty_components": comps,
                "recommended_action": f"Thay thế/khắc phục {', '.join(comps)} và vệ sinh bo mạch",
                "risk_level": "Cao" if "nguồn" in notes.lower() or "rơi nước" in notes.lower() else "TrungBinh"
            }
            return json.dumps(res, ensure_ascii=False, indent=2)

        elif task_type == "SinhTinNhan":
            ten = data.get("ten_khach", "Quý khách")
            model = data.get("model_may", "thiết bị")
            status = data.get("trang_thai", "DangXuLy")
            cost = data.get("chi_phi", 0)
            date = data.get("ngay_hen", "trong ngày")
            
            st_map = {
                "DangKiemTra": "đang được KTV kiểm tra chi tiết",
                "DangSuaChua": "đang được tiến hành sửa chữa",
                "DaSuaXong": "đã được sửa xong và kiểm tra ổn định",
                "HoanTat_TraMay": "đã hoàn tất thủ tục bàn giao"
            }
            desc = st_map.get(status, "đang được xử lý")
            return f"PhoneCare: Chào {ten}, máy {model} của bạn {desc}. Chi phí ước tính: {cost:,.0f}đ. Hẹn trả: {date}. Hotline: 1900.6868."

        elif task_type == "GiaiThichDichVu":
            dv = data.get("ten_dich_vu", "Sửa chữa")
            lk = data.get("ten_linh_kien", "Linh kiện")
            loi = data.get("loi_thuc_te", "hỏng hóc")
            return f"Thiết bị gặp hiện tượng: '{loi}'. Việc thực hiện '{dv}' nhằm thay thế '{lk}' bị suy hao, giúp máy khôi phục chức năng và tránh ảnh hưởng chập cháy sang các linh kiện quan trọng khác trên bo mạch."

        return "Phản hồi mặc định từ hệ thống."

    @staticmethod
    def _log_ai_request(phieu_id: Optional[int], task_type: str, prompt: str, raw_response: str, parsed_json: str, exec_time_ms: float, status: str):
        """Ghi vết Audit log tự động vào CSDL."""
        db = SessionLocal()
        try:
            log_entry = NhatKyAI(
                phieu_sua_chua_id=phieu_id,
                loai_tac_vu=task_type,
                model_name=settings.GEMINI_MODEL_NAME,
                prompt_input=prompt,
                ai_raw_response=raw_response,
                ai_parsed_json=parsed_json,
                execution_time_ms=exec_time_ms,
                trang_thai=status
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            print(f"[Audit Log Error] Không thể ghi log AI: {e}")
        finally:
            db.close()

    # --- Các phương thức giao tiếp công khai ---

    @classmethod
    def summarize_fault(cls, model_may: str, mo_ta_loi_khach: str, ghi_chu_ky_thuat: str, phieu_id: Optional[int] = None) -> Dict[str, Any]:
        """Kích hoạt FR-10: Tóm tắt lỗi từ ghi chú KTV."""
        clean_notes = DataSanitizer.sanitize(ghi_chu_ky_thuat)
        clean_desc = DataSanitizer.sanitize(mo_ta_loi_khach)
        prompt = PromptTemplates.get_fault_summary_prompt(model_may, clean_desc, clean_notes)
        fallback_data = {
            "phieu_id": phieu_id,
            "model_may": model_may,
            "mo_ta_loi_khach": clean_desc,
            "ghi_chu_ky_thuat": clean_notes
        }
        return cls._call_gemini_or_fallback(prompt, "TomTatLoi", fallback_data)

    @classmethod
    def generate_progress_message(cls, ten_khach: str, model_may: str, trang_thai: str, chi_phi: float, ngay_hen: str, kenh_gui: str = "SMS", phieu_id: Optional[int] = None) -> Dict[str, Any]:
        """Kích hoạt FR-11: Sinh tin nhắn tiến độ."""
        clean_name = DataSanitizer.sanitize(ten_khach)
        prompt = PromptTemplates.get_progress_message_prompt(clean_name, model_may, trang_thai, chi_phi, ngay_hen, kenh_gui)
        fallback_data = {
            "phieu_id": phieu_id,
            "ten_khach": clean_name,
            "model_may": model_may,
            "trang_thai": trang_thai,
            "chi_phi": chi_phi,
            "ngay_hen": ngay_hen,
            "kenh_gui": kenh_gui
        }
        return cls._call_gemini_or_fallback(prompt, "SinhTinNhan", fallback_data)

    @classmethod
    def explain_service(cls, ten_dich_vu: str, ten_linh_kien: str, loi_thuc_te: str, phieu_id: Optional[int] = None) -> Dict[str, Any]:
        """Kích hoạt FR-12: Giải thích lỗi & dịch vụ cho khách."""
        clean_fault = DataSanitizer.sanitize(loi_thuc_te)
        prompt = PromptTemplates.get_service_explanation_prompt(ten_dich_vu, ten_linh_kien, clean_fault)
        fallback_data = {
            "phieu_id": phieu_id,
            "ten_dich_vu": ten_dich_vu,
            "ten_linh_kien": ten_linh_kien,
            "loi_thuc_te": clean_fault
        }
        return cls._call_gemini_or_fallback(prompt, "GiaiThichDichVu", fallback_data)
