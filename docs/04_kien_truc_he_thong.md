# 4. THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

## 4.1. Tổng quan Kiến trúc Đa Tầng (Multi-Tier Architecture)

Hệ thống được thiết kế theo kiến trúc phân tầng hiện đại (Clean Multi-Tier Architecture), phân tách độc lập giữa Tầng trình diễn (Presentation Layer), Tầng nghiệp vụ API (Backend Layer), Tầng AI Orchestration và Tầng dữ liệu (Database Layer).

```
+-----------------------------------------------------------------------------------------------+
| 1. TẦNG TRÌNH DIỄN (PRESENTATION LAYER)                                                       |
|   - Giao diện Cổng Quản trị & Nghiệp vụ nội bộ (Admin, Lễ tân, KTV, Thu ngân)                |
|   - Cổng Khách hàng Tra cứu Tiến độ Trực tuyến (QR Code Tra cứu & Giải thích lỗi)             |
|   - Công nghệ: HTML5, CSS3 Modern Glassmorphism/Dark Theme, JavaScript (Async Fetch API)      |
+-----------------------------------------------------------------------------------------------+
                                                |
                                    HTTPS / RESTful API / JSON
                                                v
+-----------------------------------------------------------------------------------------------+
| 2. TẦNG DỊCH VỤ & NGHIỆP VỤ (BACKEND API - FASTAPI)                                           |
|   - API Gateway & Authentication: JWT Bearer Token + Role-Based Access Control (RBAC)         |
|   - Module Tiếp nhận & Khách hàng: Customer, Device Management                                |
|   - Module Sửa chữa & Điều phối: Repair Order Lifecycle Engine (8 Trạng thái)                 |
|   - Module Kho linh kiện & Dịch vụ: Inventory Control & Pricing                               |
|   - Module Hóa đơn & Bảo hành: Invoicing & Warranty Tracking                                  |
|   - Module Thống kê & Báo cáo: Analytics & Reporting                                          |
|                                                                                               |
|   +---------------------------------------------------------------------------------------+   |
|   | 2.1 AI ORCHESTRATION & PROMPT MANAGEMENT SERVICE                                      |   |
|   |   - Data Sanitization Layer (Bóc tách dữ liệu PII nhạy cảm trước khi gọi AI)         |   |
|   |   - Prompt Template Manager (Quản lý 3 bộ prompt chuẩn 5 thành phần & Guardrails)     |   |
|   |   - JSON Parser & Pydantic Schema Validator                                           |   |
|   |   - Fallback Strategy & Exception Handler (Timeout 5s, Regex Repair, Static Template) |   |
|   |   - AI Audit Logger (Tự động ghi vết vào bảng NhatKyAI)                               |   |
|   +---------------------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------------------+
                 |                                                      |
    SQLAlchemy ORM / SQLite DB Driver                         HTTPS POST / Payload JSON
                 v                                                      v
+----------------------------------------+             +----------------------------------------+
| 3. TẦNG DỮ LIỆU (DATABASE LAYER)       |             | 4. TẦNG DỊCH VỤ AI (AI CLOUD SERVICE)  |
|   - Hệ quản trị CSDL SQLite            |             |   - Google Gemini 1.5 Flash / Pro API  |
|   - File CSDL: phone_repair.db         |             |   - JSON Structured Output Mode        |
|   - 10 Bảng quan hệ toàn vẹn           |             |   - Anti-Hallucination Guardrails      |
|   - Backup định kỳ hàng ngày           |             +----------------------------------------+
+----------------------------------------+
```

## 4.2. Chi tiết các Phân hệ & Trách nhiệm

1. **Presentation Layer**:
   - Giao diện thân thiện, hiển thị trực quan thông tin tiến độ của từng thiết bị.
   - Hộp thoại tương tác AI (AI Sandbox / Suggestions) cho phép KTV và Lễ tân xem trước gợi ý của AI, chỉnh sửa nội dung trước khi lưu chính thức (nguyên tắc Human-in-the-loop).
2. **FastAPI Backend**:
   - Tận dụng tính bất đồng bộ (Asynchronous async/await) cho hiệu năng cao và tốc độ xử lý nhanh.
   - Pydantic models giúp kiểm soát chặt chẽ kiểu dữ liệu đầu vào và đầu ra.
   - Tự động sinh tài liệu API tương tác tại `/docs` (OpenAPI Swagger UI).
3. **AI Orchestration Layer**:
   - Đóng vai trò cầu nối an toàn giữa CSDL nội bộ và Google Gemini LLM.
   - Chịu trách nhiệm bảo vệ dữ liệu khách hàng qua lớp làm sạch PII.
   - Đảm bảo đầu ra JSON luôn tuân thủ schema quy định trước khi trả về cho tầng ứng dụng.
4. **Database Layer**:
   - Sử dụng SQLite thông qua SQLAlchemy ORM, đảm bảo tính gọn nhẹ, dễ triển khai kiểm thử và tương thích cao khi chuyển đổi sang PostgreSQL/MySQL ở môi trường sản xuất lớn.
