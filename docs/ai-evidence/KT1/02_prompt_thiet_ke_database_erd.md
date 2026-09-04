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

### 3. ĐÁNH GIÁ, PHẢN BIỆN VÀ HIỆU CHỈNH CỦA SINH VIÊN (Human Review & Refine)

| Thành phần | AI đề xuất ban đầu | Đánh giá của Sinh viên | Quyết định điều chỉnh / Bác bỏ |
|---|---|---|---|
| **Quản lý Tiền công & Linh kiện** | Gộp chung tổng tiền vào bảng `REPAIR_TICKETS`, bảng `PARTS` chỉ chứa linh kiện thay thế. | Thiếu phân biệt giữa tiền mua vật tư linh kiện và tiền công thợ sửa chữa (dịch vụ kỹ thuật); không lưu được lịch sử giá lúc sửa. | **BỔ SUNG BẢNG MỚI**: Tách thành 2 danh mục riêng biệt: `linh_kien` (quản lý tồn kho) và `dich_vu` (bảng giá tiền công). Tạo bảng liên kết `chi_tiet_sua_chua` lưu đơn giá tại thời điểm lập phiếu. |
| **Quản lý Bảo hành** | AI không tạo bảng bảo hành mà chỉ dựa vào ngày thanh toán của hóa đơn. | Không quản lý được các linh kiện có thời hạn bảo hành khác nhau trong cùng 1 máy (ví dụ: Màn hình BH 3 tháng, Pin BH 12 tháng). | **BỔ SUNG BẢNG `bao_hanh`**: Quản lý mã bảo hành điện tử, ngày hết hạn độc lập cho từng linh kiện/dịch vụ, trạng thái `ConHan`/`HetHan`/`TuChoi`. |
| **Lưu vết hoạt động AI** | Chưa có bảng lưu log AI. | Vi phạm tiêu chí kiểm tra và audit AI an toàn của môn học. | **BỔ SUNG BẢNG `nhat_ky_ai` (`ai_logs`)**: Lưu chi tiết `phieu_sua_chua_id`, `loai_tac_vu`, `prompt_input` (đã làm sạch PII), `ai_raw_response`, `ai_parsed_json`, `execution_time_ms`, `trang_thai` (`ThanhCong`/`Fallback`). |
| **Lưu ảnh hiện trạng tiếp nhận** | AI bỏ qua trường lưu ảnh. | Khi khách mang máy vỡ màn/trầy xước đến sửa, nếu không có ảnh lưu lại lúc tiếp nhận sẽ dễ xảy ra tranh chấp ngoại quan khi trả máy. | **BỔ SUNG CỘT `hinh_anh`**: Thêm cột lưu Base64/URL ảnh hiện trạng thiết bị khi lễ tân tiếp nhận vào bảng `phieu_sua_chua`. |
