# 🤖 MINH CHỨNG SỬ DỤNG AI TRONG THIẾT KẾ PROMPT 5 THÀNH PHẦN & AN TOÀN AI (KT1)
> **Nhiệm vụ**: Xây dựng 3 bộ System/User Prompt chuẩn 5 thành phần và thiết kế cơ chế bảo vệ PII + Semantic Fallback.

---

### 1. PROMPT GỬI AI (Claude 3.5 Sonnet / Gemini 1.5 Pro)
```text
Bạn là chuyên gia Kỹ thuật Prompt (Prompt Engineer) và Bảo mật AI (AI Security).
Tôi đang xây dựng phân hệ AI cho phần mềm quản lý sửa chữa điện thoại gồm 3 vị trí:
1. AI Tóm tắt tình trạng lỗi cho KTV.
2. AI Sinh tin nhắn tiến độ SMS/Zalo cho Lễ tân.
3. AI Diễn giải dịch vụ đời thường cho Khách hàng.

Yêu cầu:
- Thiết kế Prompt theo chuẩn 5 thành phần: Instructions, Context, Constraints, Examples, Output Format.
- Đảm bảo đầu ra trả về JSON Schema nghiêm ngặt.
- Đề xuất các rủi ro bảo mật (Prompt Injection, rò rỉ dữ liệu cá nhân PII) và giải pháp phòng thủ.
```

---

### 2. PHẢN HỒI GỐC CỦA AI (Tóm tắt Output)
* **AI đề xuất cấu trúc prompt chung**:
  - Prompt tóm tắt lỗi trả về đoạn văn bản Markdown tự do.
  - Phân tích rủi ro: Người dùng có thể nhập các câu lệnh độc hại (`Ignore instructions...`) hoặc truyền trực tiếp số điện thoại khách vào LLM.

---

### 3. ĐÁNH GIÁ, PHẢN BIỆN VÀ HIỆU CHỈNH CỦA KỸ SƯ (Human Review & Refine)

| Thành phần | AI đề xuất ban đầu | Đánh giá của Kỹ sư | Quyết định điều chỉnh / Bác bỏ |
|---|---|---|---|
| **Định dạng Output** | AI đề xuất trả về Markdown tự do có bullet points. | Frontend rất khó parse để render vào form hoặc lưu vào các cột CSDL có cấu trúc. | **SỬA ĐỔI THÀNH STRICT JSON SCHEMA**: Ép buộc Gemini trả về đúng các key: `nguyen_nhan_chinh`, `cac_buoc_kiem_tra`, `linh_kien_nghi_ngo`, `muc_do_nghiem_trong`, `canh_bao_an_toan`. |
| **Bảo vệ dữ liệu cá nhân (PII)** | AI chỉ cảnh báo chung về rủi ro vi phạm GDPR/Privacy. | Thiếu giải pháp code cụ thể để chặn dữ liệu PII trước khi gửi đến Google Cloud. | **LẬP TRÌNH MODULE `DataSanitizer`**: Sử dụng Regex tự động ẩn danh hóa SĐT (thay bằng `09xxxxxxxx`), ẩn danh số IMEI (thay bằng `3548xxxxxxxxx`) và mật khẩu trước khi đưa vào payload prompt. |
| **Xử lý khi mất kết nối / Timeout** | AI đề xuất retry 3 lần liên tục. | Nếu Cloud AI bị sập hoặc quá tải, retry 3 lần sẽ khiến hệ thống bị treo (freeze) 15 giây, làm nghẽn quầy tiếp nhận. | **XÂY DỰNG `Semantic Fallback Engine`**: Cài đặt timeout 5.0s; nếu AI không phản hồi kịp hoặc lỗi mạng, tự động chuyển sang bộ quy tắc tra cứu tĩnh cục bộ (Rule-based) để trả kết quả chuẩn xác ngay lập tức. |
