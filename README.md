# 📱 HỆ THỐNG QUẢN LÝ TRUNG TÂM SỬA CHỮA ĐIỆN THOẠI TÍCH HỢP AI
> **BÀI KIỂM TRA THƯỜNG XUYÊN 1 (KT1) - BÁO CÁO PHÂN TÍCH THIẾT KẾ & KHUNG MÃ NGUỒN CHUẨN**

Dự án phát triển phần mềm quản lý toàn diện trung tâm sửa chữa điện thoại di động tích hợp trợ lý Trí tuệ Nhân tạo (Google Gemini AI), áp dụng mô hình phát triển phần mềm có AI đồng hành (**AI-Augmented SDLC**) theo chuẩn giáo trình Công nghệ Phần mềm & Kỹ thuật Thiết kế Prompt.

---

## 🌟 1. Tổng Quan Đáp Ứng 10 Tiêu Chí KT1

| Tiêu Chí KT1 | Nội Dung Đã Hiện Thực Trong Dự Án | Minh Chứng File / Module |
|---|---|---|
| **TC1: Phân tích bài toán quản lý** | Bối cảnh trung tâm bảo dưỡng sửa chữa, 5 tác nhân (Quản lý, Lễ tân, KTV, Thu ngân, Khách hàng), 8 trạng thái vòng đời, 3 điểm nghẽn nghiệp vụ và giải pháp AI. | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **TC2: Xác định yêu cầu chức năng (FRs)** | Đặc tả chi tiết 12 yêu cầu chức năng (FR-01 đến FR-12) với đầy đủ Dữ liệu vào (Input), Xử lý (Processing) và Đầu ra (Output). | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **TC3: Xác định yêu cầu phi chức năng (NFRs)** | Đặc tả bảo mật JWT, RBAC 4 vai trò, lớp ẩn danh hóa PII (`DataSanitizer`), cô lập API Key, thời gian đáp ứng API <200ms, AI timeout 5s. | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **TC4: Thiết kế Actor và Use Case** | 5 Tác nhân, Biểu đồ Use Case (Mermaid), Ma trận phân quyền RBAC và 5 đặc tả ca sử dụng chi tiết (Happy path & Exception). | [`docs/02_usecase_actor.md`](docs/02_usecase_actor.md) |
| **TC5: Thiết kế Cơ sở dữ liệu** | Sơ đồ quan hệ thực thể (ERD), Data Dictionary 10 bảng dữ liệu SQLite, ràng buộc khóa chính/ngoại, Unique và Check. | [`docs/03_database_design.md`](docs/03_database_design.md) |
| **TC6: Thiết kế Kiến trúc hệ thống** | Kiến trúc Multi-tier (Presentation, FastAPI Backend, AI Orchestrator & Guardrails, SQLite DB, Google Gemini Cloud). | [`docs/04_kien_truc_he_thong.md`](docs/04_kien_truc_he_thong.md) |
| **TC7: Xác định 3 vị trí ứng dụng AI** | (1) AI Tóm tắt tình trạng máy từ ghi chú KTV, (2) AI Sinh tin nhắn tiến độ SMS/Zalo, (3) AI Diễn giải lỗi & dịch vụ đời thường. | [`docs/05_thiet_ke_prompt_va_luong_ai.md`](docs/05_thiet_ke_prompt_va_luong_ai.md) |
| **TC8: Thiết kế Prompt 5 thành phần** | 3 bộ Prompt chuẩn 5 thành phần (Instructions, Context, Constraints, Examples, Output Format), Sequence Diagram, HITL & Fallback. | [`docs/05_thiet_ke_prompt_va_luong_ai.md`](docs/05_thiet_ke_prompt_va_luong_ai.md) |
| **TC9: Minh chứng sử dụng AI (AI Log)** | Bảng Nhật ký AI Usage Log theo chuẩn môn học: Thời gian, Nhiệm vụ, Prompt, Phản hồi AI, Đánh giá và Hiệu chỉnh con người. | [`docs/06_nhat_ky_su_dung_ai.md`](docs/06_nhat_ky_su_dung_ai.md) |
| **TC10: Tài liệu & Kế hoạch KT2, KT3** | Báo cáo kỹ thuật tổng hợp [`BAO_CAO_KT1_PHAN_TICH_THIET_KE.md`](BAO_CAO_KT1_PHAN_TICH_THIET_KE.md), cấu trúc dự án chuẩn và lộ trình chi tiết. | [`docs/07_ke_hoach_trien_khai_kt2_kt3.md`](docs/07_ke_hoach_trien_khai_kt2_kt3.md) |

---

## 🛠️ 2. Công Nghệ Sử Dụng (Technology Stack)
- **Backend**: Python 3.10+, **FastAPI** (Hiệu năng cao, tự động sinh OpenAPI Swagger docs).
- **Cơ sở dữ liệu**: **SQLite** thông qua **SQLAlchemy ORM** (10 Bảng quan hệ toàn vẹn).
- **AI Engine**: **Google Gemini API** (`gemini-1.5-flash` / `gemini-1.5-pro`) kết hợp cơ chế Fallback phòng thủ.
- **Frontend**: Single Page Web Application (HTML5, Vanilla Modern CSS Glassmorphism/Dark mode, JS Fetch API).
- **Bảo mật & Phân quyền**: **JWT (HS256)** + Thuật toán băm mật khẩu **bcrypt**.
- **Kiểm thử**: **Pytest** cho unit test prompt & database schema.

---

## 🚀 3. Hướng Dẫn Cài Đặt và Chạy Thử (3 Bước Đơn Giản)

### Bước 1: Cài đặt các thư viện phụ thuộc
Mở terminal tại thư mục dự án và chạy:
```bash
pip install -r requirements.txt
```

### Bước 2: Cấu hình biến môi trường (Tùy chọn)
Tạo file `.env` từ file mẫu `.env.example`:
```bash
cp .env.example .env
```
*(Lưu ý: Hệ thống đã tích hợp sẵn cơ chế **Semantic Rule-Based Fallback**, bạn có thể chạy thử nghiệm ngay cả khi chưa điền Gemini API Key!)*

### Bước 3: Khởi chạy máy chủ Backend & Giao diện
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```
- **Giao diện Ứng dụng & AI Sandbox Demo**: Truy cập [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Tài liệu API tương tác (Swagger UI)**: Truy cập [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Chạy Kiểm thử Tự động (Automated Tests):
```bash
pytest tests/ -v
# hoặc
python -m pytest tests/ -v
```


---

## 📁 4. Cấu Trúc Thư Mục Dự Án
```
du_an/
├── BAO_CAO_KT1_PHAN_TICH_THIET_KE.md    # Báo cáo kỹ thuật tổng hợp toàn diện KT1
├── docs/                                # Thư mục tài liệu đặc tả module hóa
│   ├── 01_bai_toan_va_yeu_cau.md        # Phân tích bối cảnh, 12 FRs và NFRs
│   ├── 02_usecase_actor.md              # Sơ đồ Use Case, ma trận RBAC & 5 đặc tả Use Case
│   ├── 03_database_design.md            # Sơ đồ ERD, Data Dictionary 10 bảng SQLite
│   ├── 04_kien_truc_he_thong.md         # Kiến trúc Multi-tier & Data Flow
│   ├── 05_thiet_ke_prompt_va_luong_ai.md# 3 Prompt Templates 5 thành phần, HITL, Fallback
│   ├── 06_nhat_ky_su_dung_ai.md         # Nhật ký sử dụng AI (AI Usage Log KT1)
│   └── 07_ke_hoach_trien_khai_kt2_kt3.md# Kế hoạch chi tiết KT2, KT3 & Cuối kỳ
├── backend/                             # Mã nguồn Backend FastAPI
│   └── app/
│       ├── core/                        # Cấu hình hệ thống & Security (JWT, bcrypt)
│       ├── db/                          # Database connection, Models, Seed script
│       ├── services/                    # Gemini AI Service, Prompt Templates, PII Sanitizer
│       ├── api/                         # REST API Endpoints & Routers
│       └── main.py                      # File khởi chạy ứng dụng
├── frontend/                            # Giao diện Web HTML5/CSS/JS hiện đại
│   ├── index.html                       # Dashboard phân tích thiết kế & AI Sandbox Demo
│   ├── css/style.css                    # Bảng kiểu Glassmorphism Dark Theme
│   └── js/app.js                        # Xử lý logic gọi API & tương tác
├── tests/                               # Bộ kiểm thử tự động (Pytest)
│   └── test_ai_prompts.py               # Test prompt, sanitizer & database
├── requirements.txt                     # Danh sách thư viện Python
├── .env.example                         # File mẫu cấu hình biến môi trường
└── README.md                            # Hướng dẫn dự án
```

---

## 🎯 5. Tài Khoản Đăng Nhập Mẫu Demo (Seed Data)
| Tên Đăng Nhập | Mật Khẩu | Họ Tên | Vai Trò (RBAC) | Quyền Hạn Chính |
|---|---|---|---|---|
| `admin` | `123456` | Nguyễn Văn Quản Lý | `QuanLy` | Toàn quyền cấu hình, tài khoản, xem thống kê |
| `letan` | `123456` | Trần Thị Lễ Tân | `LeTan` | Tiếp nhận máy, tạo phiếu, gửi SMS AI |
| `ktv` | `123456` | Lê Văn Kỹ Thuật | `KyThuatVien` | Chẩn đoán máy, dùng AI tóm tắt lỗi, sửa chữa |
| `thungan` | `123456` | Phạm Thị Thu Ngân | `ThuNgan` | Lập hóa đơn, thu tiền, kích hoạt bảo hành |
