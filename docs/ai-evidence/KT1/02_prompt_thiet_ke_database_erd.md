# 🤖 MINH CHỨNG SỬ DỤNG AI TRONG THIẾT KẾ CƠ SỞ DỮ LIỆU & ERD (KT1)
> **Nhiệm vụ**: Thiết kế cấu trúc cơ sở dữ liệu quan hệ (Relational Database) và sơ đồ ERD trên nền tảng SQLite + SQLAlchemy.

---

### 1. PROMPT GỬI AI (Google Gemini 1.5 Pro)
```text
Bạn là chuyên gia Cơ sở dữ liệu (Database Architect).
Dựa trên bài toán trung tâm sửa chữa điện thoại có phân quyền RBAC và phân hệ AI audit log:
Hãy đề xuất cấu trúc bảng cơ sở dữ liệu (Schema) và sơ đồ ERD dạng Mermaid cho hệ thống PhoneCare AI trên SQLite.
Yêu cầu:
- Chuẩn hóa tối thiểu dạng 3NF.
- Đầy đủ khóa chính (PK), khóa ngoại (FK), kiểu dữ liệu và ràng buộc toàn vẹn.
- Quản lý được chi phí linh kiện, tiền công dịch vụ, hóa đơn, bảo hành và vết gọi AI.
```

---

### 2. PHẢN HỒI GỐC CỦA AI (Tóm tắt Output)
* **AI đề xuất 6 bảng cơ bản**:
  1. `USERS (id, username, password, role)`
  2. `CUSTOMERS (id, name, phone, address)`
  3. `DEVICES (id, customer_id, model, imei)`
  4. `REPAIR_TICKETS (id, customer_id, device_id, issue, cost, status)`
  5. `PARTS (id, name, price, stock)`
  6. `INVOICES (id, ticket_id, total, payment_date)`

---

### 3. ĐÁNH GIÁ, PHẢN BIỆN VÀ HIỆU CHỈNH CỦA KỸ SƯ (Human Review & Refine)

| Thành phần | AI đề xuất ban đầu | Đánh giá của Kỹ sư | Quyết định điều chỉnh / Bác bỏ |
|---|---|---|---|
| **Bảng Linh kiện & Dịch vụ** | Gộp chung `chi_phi` vào bảng Phiếu sửa chữa mà không có bảng giá danh mục. | Không quản lý được tồn kho linh kiện, không phân định được tiền công thợ và tiền linh kiện. | **BỔ SUNG 2 BẢNG**: Tách thành bảng `linh_kien` (quản lý tồn kho) và `dich_vu` (quản lý đơn giá công thợ cố định). |
| **Bảo hành điện tử** | Chỉ có trường `han_bao_hanh` chung cho cả phiếu. | Mỗi linh kiện thay thế (pin, màn hình, cáp) có thời hạn bảo hành khác nhau (3 tháng, 6 tháng, 12 tháng). | **BỔ SUNG BẢNG `bao_hanh`**: Quản lý chi tiết từng linh kiện, ngày hết hạn và mã bảo hành tra cứu công khai. |
| **Lưu vết hoạt động AI** | Chưa có bảng lưu log AI. | Vi phạm tiêu chuẩn an toàn thông tin và audit AI trong doanh nghiệp. | **BỔ SUNG BẢNG `nhat_ky_ai` (`ai_logs`)**: Lưu chi tiết `phieu_sua_chua_id`, `loai_tac_vu`, `prompt_input` (đã làm sạch PII), `ai_raw_response`, `ai_parsed_json`, `execution_time_ms`, `trang_thai` (`ThanhCong`/`Fallback`). |
| **Lưu ảnh hiện trạng tiếp nhận** | AI bỏ qua trường lưu ảnh. | Khi khách mang máy vỡ màn/trầy xước đến sửa, nếu không có ảnh lưu lại lúc tiếp nhận sẽ dễ xảy ra tranh chấp ngoại quan khi trả máy. | **BỔ SUNG CỘT `hinh_anh`**: Thêm cột lưu Base64/URL ảnh hiện trạng thiết bị khi lễ tân tiếp nhận vào bảng `phieu_sua_chua`. |
