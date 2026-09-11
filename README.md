# 📱 PHONECARE AI — HỆ THỐNG QUẢN LÝ TRUNG TÂM SỬA CHỮA ĐIỆN THOẠI TÍCH HỢP AI

> Hệ thống Quản lý Dịch vụ Sửa chữa Thiết bị Di động Toàn diện được xây dựng trên nền tảng **FastAPI (Python 3.12)**, **Modular Web Architecture (ES6+ & Modern CSS3)**, **SQLite / SQLAlchemy ORM** và **Google Gemini AI**.

[![Backend FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Frontend Modern](https://img.shields.io/badge/Frontend-ES6+_|_CSS3_Modular-61DAFB?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org)
[![Server Uvicorn](https://img.shields.io/badge/Server-Uvicorn_ASGI-495057?style=flat-square&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)
[![Database SQLite](https://img.shields.io/badge/Database-SQLite_3_|_SQLAlchemy-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![AI Engine Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-8E75C2?style=flat-square&logo=googlegemini&logoColor=white)](https://ai.google.dev)
[![Architecture RAG](https://img.shields.io/badge/Architecture-Enterprise_RAG_Pipeline-4CAF50?style=flat-square&logo=probot&logoColor=white)](#)
[![Tests Passed](https://img.shields.io/badge/Tests-22_Passed-brightgreen?style=flat-square&logo=pytest&logoColor=white)](#)
[![License MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

Dự án phát triển nền tảng phần mềm quản lý toàn diện trung tâm bảo hành, sửa chữa thiết bị di động tích hợp trợ lý Trí tuệ Nhân tạo (Google Gemini AI), áp dụng mô hình phát triển phần mềm hiện đại có AI đồng hành (**AI-Augmented SDLC**) theo chuẩn kiến trúc doanh nghiệp kết hợp kỹ thuật Prompt Engineering & Guardrails an toàn dữ liệu.

---

## 🌟 1. Các Trụ Cột Kỹ Thuật & Kiến Trúc Nền Tảng (Core Architecture Pillars)

| Trụ Cột Kỹ Thuật | Nội Dung & Giải Pháp Hiện Thực | Tài Liệu & Module Nguồn |
|---|---|---|
| **1. Khảo sát & Phân tích nghiệp vụ** | Bối cảnh trung tâm dịch vụ, 5 tác nhân (Quản lý, Lễ tân, KTV, Thu ngân, Khách hàng), 8 trạng thái vòng đời, giải quyết 3 điểm nghẽn vận hành bằng AI. | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **2. Yêu cầu chức năng nghiệp vụ (FRs)** | Đặc tả chi tiết 12 yêu cầu chức năng (FR-01 đến FR-12) với đầy đủ Dữ liệu vào (Input), Xử lý (Processing) và Đầu ra (Output). | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **3. Yêu cầu phi chức năng & Bảo mật (NFRs)** | Đặc tả bảo mật JWT, RBAC 4 vai trò, lớp ẩn danh hóa PII (`DataSanitizer`), cô lập API Key, thời gian đáp ứng API <200ms, AI timeout 5s. | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **4. Mô hình tác nhân & Phân quyền RBAC** | 5 Tác nhân, Biểu đồ Use Case (Mermaid), Ma trận phân quyền RBAC và 5 đặc tả ca sử dụng chi tiết (Happy path & Exception). | [`docs/02_usecase_actor.md`](docs/02_usecase_actor.md) |
| **5. Thiết kế Cơ sở dữ liệu quan hệ** | Sơ đồ quan hệ thực thể (ERD), Data Dictionary 10 bảng dữ liệu SQLite, ràng buộc khóa chính/ngoại, Unique và Check constraints. | [`docs/03_database_design.md`](docs/03_database_design.md) |
| **6. Kiến trúc hệ thống đa tầng** | Kiến trúc Multi-tier (Presentation, FastAPI Backend, AI Orchestrator & Guardrails, SQLite DB, Google Gemini Cloud). | [`docs/04_kien_truc_he_thong.md`](docs/04_kien_truc_he_thong.md) |
| **7. Phân hệ trợ lý AI chuyên sâu** | (1) AI Tóm tắt tình trạng máy từ ghi chú KTV, (2) AI Sinh tin nhắn tiến độ SMS/Zalo, (3) AI Diễn giải lỗi & dịch vụ bằng ngôn ngữ đời thường. | [`docs/05_thiet_ke_prompt_va_luong_ai.md`](docs/05_thiet_ke_prompt_va_luong_ai.md) |
| **8. Kỹ thuật Prompt Engineering & An toàn** | 3 bộ Prompt chuẩn 5 thành phần (Instructions, Context, Constraints, Examples, Output Format), Sequence Diagram, Human-in-the-loop (HITL) & Fallback Engine. | [`docs/05_thiet_ke_prompt_va_luong_ai.md`](docs/05_thiet_ke_prompt_va_luong_ai.md) |
| **9. Nhật ký tương tác & Giám sát AI** | Bảng Nhật ký AI Usage Log & Giám sát mô hình: Thời gian, Nhiệm vụ, Prompt, Phản hồi AI, Đánh giá và Phê duyệt con người (AI Observability). | [`docs/06_nhat_ky_su_dung_ai.md`](docs/06_nhat_ky_su_dung_ai.md) |
| **10. Tài liệu kỹ thuật & Kế hoạch mở rộng** | Báo cáo kỹ thuật tổng hợp [`BAO_CAO_KT1_PHAN_TICH_THIET_KE.md`](BAO_CAO_KT1_PHAN_TICH_THIET_KE.md), cấu trúc dự án chuẩn và lộ trình phát triển tính năng các giai đoạn tiếp theo. | [`docs/07_ke_hoach_trien_khai_kt2_kt3.md`](docs/07_ke_hoach_trien_khai_kt2_kt3.md) |
| **11. Đánh giá & Tối ưu hóa mô hình AI** | Báo cáo thử nghiệm A/B 3 kỹ thuật (Zero-shot vs Few-shot vs CoT) trên bộ dataset 20 ca bệnh thực tế, đo lường 5 chỉ số (Accuracy 98%, Completeness 100%, Consistency 98%, Robustness 95%, Latency) và cơ chế tự phục hồi `JSONRepairEngine`. | [`docs/08_toi_uu_va_danh_gia_chat_luong_ai.md`](docs/08_toi_uu_va_danh_gia_chat_luong_ai.md) |

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
- **Giao diện Ứng dụng Quản Trị & Trợ Lý AI**: Truy cập [http://127.0.0.1:8000](http://127.0.0.1:8000)
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
├── BAO_CAO_KT1_PHAN_TICH_THIET_KE.md    # Báo cáo kỹ thuật phân tích thiết kế toàn diện
├── docs/                                # Thư mục tài liệu đặc tả module hóa
│   ├── 01_bai_toan_va_yeu_cau.md        # Phân tích bối cảnh, 12 FRs và NFRs
│   ├── 02_usecase_actor.md              # Sơ đồ Use Case, ma trận RBAC & 5 đặc tả Use Case
│   ├── 03_database_design.md            # Sơ đồ ERD, Data Dictionary 10 bảng SQLite
│   ├── 04_kien_truc_he_thong.md         # Kiến trúc Multi-tier & Data Flow
│   ├── 05_thiet_ke_prompt_va_luong_ai.md# 3 Prompt Templates 5 thành phần, HITL, Fallback
│   ├── 06_nhat_ky_su_dung_ai.md         # Nhật ký tương tác & giám sát AI (AI Usage Log)
│   ├── 07_ke_hoach_trien_khai_kt2_kt3.md# Kế hoạch lộ trình phát triển & mở rộng tính năng
│   └── 08_toi_uu_va_danh_gia_chat_luong_ai.md# Báo cáo Benchmark 20 ca bệnh, A/B testing 3 kỹ thuật
├── backend/                             # Mã nguồn Backend FastAPI
│   └── app/
│       ├── core/                        # Cấu hình hệ thống & Security (JWT, bcrypt)
│       ├── db/                          # Database connection, Models, Seed script
│       ├── services/                    # Gemini AI Service, RAG Engine, Benchmark Service
│       ├── api/                         # REST API Endpoints & Routers
│       └── main.py                      # File khởi chạy ứng dụng
├── frontend/                            # Giao diện Web HTML5/CSS/JS hiện đại
│   ├── index.html                       # Dashboard quản trị trung tâm & Trợ lý AI
│   ├── css/                             # Bảng kiểu Glassmorphism Dark Theme
│   └── js/                              # Xử lý logic gọi API & tương tác
├── tests/                               # Bộ kiểm thử tự động toàn diện (32 Pytest Cases)
│   ├── test_crud_rbac.py                # Test CRUD và phân quyền 4 vai trò
│   ├── test_ai_prompts.py               # Test 3 chức năng AI & PII Sanitizer
│   ├── test_rag_pipeline.py             # Test luồng RAG Tri thức & A/B Tuning
│   └── test_ai_benchmark_and_robustness.py# Test 20 ca bệnh, JSON repair & injection defense
├── requirements.txt                     # Danh sách thư viện Python
├── .env.example                         # File mẫu cấu hình biến môi trường
└── README.md                            # Hướng dẫn dự án
```

---

## 🎯 5. Tài Khoản Đăng Nhập Khởi Tạo (Seed Data)
| Tên Đăng Nhập | Mật Khẩu | Họ Tên | Vai Trò (RBAC) | Quyền Hạn Chính |
|---|---|---|---|---|
| `admin` | `123456` | Nguyễn Hoàng Long | `QuanLy` | Toàn quyền cấu hình, tài khoản, xem thống kê |
| `letan` | `123456` | Trần Mai Phương | `LeTan` | Tiếp nhận máy, tạo phiếu, gửi SMS AI |
| `ktv` | `123456` | Lê Quốc Cường | `KyThuatVien` | Chẩn đoán máy, dùng AI tóm tắt lỗi, sửa chữa |
| `thungan` | `123456` | Phạm Thanh Hà | `ThuNgan` | Lập hóa đơn, thu tiền, kích hoạt bảo hành |
