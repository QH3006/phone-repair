# 📝 TÀI LIỆU HƯỚNG DẪN & NỘI DUNG CHI TIẾT CẦN CHỈNH SỬA BÁO CÁO (PDF 45 TRANG)

> **Mục đích:** Cung cấp đầy đủ các đoạn văn bản, bảng biểu đã chuẩn hóa và hướng dẫn thao tác cụ thể theo từng số trang trong file báo cáo để bạn dễ dàng copy - paste vào Microsoft Word.
> **Giải quyết triệt để 2 nhược điểm giảng viên đã nhận xét:**
> 1. Thiếu file chuẩn mang tên `ai_log.md` (đã bổ sung dẫn chiếu và cập nhật cây thư mục).
> 2. Tài liệu hơi tham phạm vi (đã bổ sung mục phân định ranh giới phạm vi rõ ràng).

---

## 📌 MỤC LỤC CÁC PHẦN CẦN CHỈNH SỬA

1. [VỊ TRÍ 1 - TRANG 5 & 6: Bổ sung mục Phân định Ranh giới Phạm vi](#vị-trí-1---trang-5--6-bổ-sung-mục-phân-định-ranh-giới-phạm-vi)
2. [VỊ TRÍ 2 - TRANG 16 & 21: Khắc phục lỗi trang trắng mồ côi (Use Case 1 & 5)](#vị-trí-2---trang-16--21-khắc-phục-lỗi-trang-trắng-mồ-côi-use-case-1--5)
3. [VỊ TRÍ 3 - TRANG 26 & 27: Kẻ lại bảng chuẩn cho Bảng 5, 6, 7, 8, 9 CSDL](#vị-trí-3---trang-26--27-kẻ-lại-bảng-chuẩn-cho-bảng-5-6-7-8-9-csdl)
4. [VỊ TRÍ 4 - TRANG 37, 38, 39: Chỉnh sửa Mục 10 (Dẫn chiếu `ai_log.md`)](#vị-trí-4---trang-37-38-39-chỉnh-sửa-mục-10-dẫn-chiếu-ai_logmd)
5. [VỊ TRÍ 5 - TRANG 40 & 41: Cập nhật Cây thư mục dự án (Mục 11.1)](#vị-trí-5---trang-40--41-cập-nhật-cây-thư-mục-dự-án-mục-111)
6. [VỊ TRÍ 6 - TRANG 42 ĐẾN 45: Cập nhật 35 Test Cases kiểm thử tự động (Mục 11.3)](#vị-trí-6---trang-42-đến-45-cập-nhật-35-test-cases-kiểm-thử-tự-động-mục-113)
7. [VỊ TRÍ 7 - TRANG 45: Cập nhật phần Kết luận (Mục 12)](#vị-trí-7---trang-45-cập-nhật-phần-kết-luận-mục-12)

---

## 1. VỊ TRÍ 1 - TRANG 5 & 6: BỔ SUNG MỤC PHÂN ĐỊNH RANH GIỚI PHẠM VI

*👉 **Vị trí chèn:** Chèn vào ngay sau gạch đầu dòng cuối cùng của Mục **1.2. Mục tiêu của đề tài** (trước khi sang Mục 2).*

### Đoạn văn bản cần copy vào Word:

> **Phân định ranh giới phạm vi kỹ thuật (Scope Boundary):**  
> Nhằm tập trung tối đa nguồn lực vào chất lượng vận hành thực tế và giải quyết hiện tượng "tham phạm vi", đồ án phân định rõ ranh giới:
> - **Phạm vi CỐT LÕI (Core In-Scope — Trọng tâm đánh giá KT2):**
>   + Hoàn thiện 100% CRUD 5 phân hệ nghiệp vụ: Khách hàng & Thiết bị, Kho linh kiện & Dịch vụ, Phiếu sửa chữa & Chi tiết thay thế, Hóa đơn & Sổ bảo hành điện tử, Quản trị nhân sự.
>   + Xác thực JWT Bearer Token, băm mật khẩu bảo mật `bcrypt` và cơ chế phân quyền RBAC 4 vai trò rõ rệt (`QuanLy`, `LeTan`, `KyThuatVien`, `ThuNgan`).
>   + 3 Tính năng trợ lý AI phục vụ trực tiếp quy trình sửa chữa: Tóm tắt bệnh máy từ ghi chú KTV, Diễn giải lỗi/dịch vụ bằng ngôn ngữ đời thường cho khách, Tự động soạn tin nhắn SMS/Zalo.
>   + Bộ kiểm thử tự động `pytest` (35 test cases) và tệp nhật ký sử dụng AI bắt buộc mang tên `ai_log.md` theo chuẩn Human-in-the-Loop.
> - **Phần mở rộng nghiên cứu (Experimental / Out-of-Scope — Tùy chọn):**
>   + Các phân hệ thử nghiệm như RAG tra cứu cẩm nang kỹ thuật hay AI Sandbox đa mô hình là phần nghiên cứu học thuật phụ trợ, được tách rời thành module độc lập, hoàn toàn không làm ảnh hưởng đến luồng vận hành nghiệp vụ CRUD cốt lõi.

---

## 2. VỊ TRÍ 2 - TRANG 16 & 21: KHẮC PHỤC LỖI TRANG TRẮNG MỒ CÔI (USE CASE 1 & 5)

*👉 **Hiện tượng:** Trang 16 chỉ có 2 dòng chữ rồi trắng tinh cả trang. Trang 21 chỉ có đúng 1 dòng chữ rồi trắng tinh cả trang.*

### Cách xử lý trên Microsoft Word:
1. **Bật hiển thị ký tự ẩn:** Trong tab **Home**, bấm vào biểu tượng `¶` (Show/Hide Formatting Marks).
2. **Xóa ngắt trang thừa:** Nếu thấy có dòng `---------- Page Break ----------` ở ngay dưới tiêu đề Use Case 1 (trang 16) hoặc Use Case 5 (trang 21), hãy bấm chuột vào và nhấn phím **Delete** để xóa đi.
3. **Thu nhỏ kích thước hình ảnh:**
   - Click chuột phải vào hình sơ đồ Use Case Lễ tân (Trang 17) $\rightarrow$ chọn **Size and Position...** $\rightarrow$ giảm chiều cao xuống khoảng **13cm - 14cm** (Scale khoảng 75% - 80%).
   - Tương tự với sơ đồ Use Case Thu ngân (Trang 22) $\rightarrow$ giảm chiều cao xuống khoảng **13cm - 14cm**.
4. **Kết quả:** Tiêu đề Use Case 1 và sơ đồ sẽ cùng nằm gọn gàng trong Trang 16; Tiêu đề Use Case 5 và sơ đồ sẽ cùng nằm gọn trong Trang 20/21. Hai trang trắng thừa thãi sẽ **biến mất 100%**.

---

## 3. VỊ TRÍ 3 - TRANG 26 & 27: KẺ LẠI BẢNG CHUẨN CHO BẢNG 5, 6, 7, 8, 9 CSDL

*👉 **Vị trí thay thế:** Xóa các dòng chữ liệt kê thô sơ từ Bảng 5 đến Bảng 9 ở Mục 6.1 (Trang 26 và 27), thay bằng các bảng kẻ chuẩn chỉn chu dưới đây (đồng bộ phong cách với Bảng 1, 2, 3, 4).*

### 5. Bảng `LinhKien` (Kho linh kiện)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Mã định danh linh kiện |
| `ma_linh_kien` | VARCHAR(50) | UNIQUE, NOT NULL | Mã SKU quản lý kho |
| `ten_linh_kien` | VARCHAR(100) | NOT NULL | Tên linh kiện (Màn hình OLED, Pin, Camera,...) |
| `loai_may` | VARCHAR(50) | NOT NULL | Dòng máy tương thích (iPhone 13, Galaxy S22,...) |
| `gia_nhap` | DECIMAL(12,2) | NOT NULL, >= 0 | Giá nhập kho |
| `gia_ban` | DECIMAL(12,2) | NOT NULL, >= 0 | Giá bán linh kiện cho khách |
| `so_luong_ton` | INTEGER | NOT NULL, DEFAULT 0 | Số lượng tồn kho hiện tại (>= 0) |
| `muc_ton_toi_thieu` | INTEGER | DEFAULT 5 | Ngưỡng cảnh báo sắp hết hàng |
| `thoi_han_bao_hanh_thang` | INTEGER | DEFAULT 6 | Thời hạn bảo hành tiêu chuẩn (tháng) |

### 6. Bảng `DichVu` (Bảng giá tiền công dịch vụ kỹ thuật)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Mã định danh dịch vụ |
| `ma_dich_vu` | VARCHAR(50) | UNIQUE, NOT NULL | Mã dịch vụ kỹ thuật |
| `ten_dich_vu` | VARCHAR(100) | NOT NULL | Tên dịch vụ (Ép kính, Đóng chip, Vệ sinh sấy nước,...) |
| `gia_cong` | DECIMAL(12,2) | NOT NULL, >= 0 | Tiền công kỹ thuật viên |
| `mo_ta` | TEXT | NULLABLE | Mô tả chi tiết kỹ thuật thực hiện |

### 7. Bảng `ChiTietSuaChua` (Liên kết linh kiện & dịch vụ trong từng phiếu)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Mã định danh bản ghi chi tiết |
| `phieu_sua_chua_id` | INTEGER | FOREIGN KEY -> PhieuSuaChua(id) | Thuộc phiếu sửa chữa nào |
| `linh_kien_id` | INTEGER | FOREIGN KEY -> LinhKien(id), NULLABLE | Linh kiện xuất kho thay thế (nếu có) |
| `dich_vu_id` | INTEGER | FOREIGN KEY -> DichVu(id), NULLABLE | Tiền công dịch vụ áp dụng (nếu có) |
| `so_luong` | INTEGER | NOT NULL, DEFAULT 1 | Số lượng thay thế |
| `don_gia` | DECIMAL(12,2) | NOT NULL | Đơn giá tại thời điểm áp dụng |
| `thanh_tien` | DECIMAL(12,2) | NOT NULL | Thành tiền (`so_luong * don_gia`) |

### 8. Bảng `HoaDon` & Bảng `BaoHanh` (Thanh toán & Thẻ bảo hành điện tử)

#### Bảng `HoaDon` (Hóa đơn thanh toán)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Mã định danh hóa đơn |
| `ma_hoa_don` | VARCHAR(30) | UNIQUE, NOT NULL | Mã hóa đơn hiển thị (HD-YYYYMMDD-XXX) |
| `phieu_sua_chua_id` | INTEGER | FOREIGN KEY -> PhieuSuaChua(id) | Phiếu sửa chữa được thanh toán |
| `thu_ngan_id` | INTEGER | FOREIGN KEY -> NguoiDung(id) | Thu ngân lập hóa đơn |
| `tong_tien` | DECIMAL(12,2) | NOT NULL | Tổng tiền thực thu |
| `phuong_thuc_tt` | VARCHAR(30) | NOT NULL | `TienMat` hoặc `ChuyenKhoan_VietQR` |
| `trang_thai_tt` | VARCHAR(30) | NOT NULL, DEFAULT 'DaThanhToan' | Trạng thái thanh toán |
| `ngay_thanh_toan` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Thời gian thanh toán |

#### Bảng `BaoHanh` (Sổ bảo hành điện tử)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Mã định danh bảo hành |
| `ma_bao_hanh` | VARCHAR(30) | UNIQUE, NOT NULL | Mã thẻ BH điện tử (BH-YYYYMMDD-XXX) |
| `phieu_sua_chua_id` | INTEGER | FOREIGN KEY -> PhieuSuaChua(id) | Phiếu sửa gốc liên quan |
| `linh_kien_id` | INTEGER | FOREIGN KEY -> LinhKien(id) | Linh kiện được bảo hành |
| `ngay_bat_dau` | DATETIME | NOT NULL | Ngày kích hoạt bảo hành |
| `ngay_het_han` | DATETIME | NOT NULL | Ngày hết hạn bảo hành |
| `trang_thai` | VARCHAR(20) | DEFAULT 'ConHan' | `ConHan` hoặc `HetHan` |

### 9. Bảng `NhatKyAI` (Kiểm toán & Audit Log AI)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Mã định danh log AI |
| `phieu_sua_chua_id` | INTEGER | FOREIGN KEY, NULLABLE | Phiếu sửa chữa liên quan |
| `loai_tac_vu` | VARCHAR(50) | NOT NULL | `TomTatLoi`, `SinhTinNhan`, `GiaiThichDichVu` |
| `model_name` | VARCHAR(50) | NOT NULL | Model LLM sử dụng (Gemini 1.5 Flash / Pro) |
| `prompt_input` | TEXT | NOT NULL | Nội dung Prompt đã làm sạch PII |
| `ai_raw_response` | TEXT | NULLABLE | Phản hồi thô nguyên bản từ API |
| `ai_parsed_json` | TEXT | NULLABLE | Dữ liệu JSON sau khi validate schema |
| `execution_time_ms` | INTEGER | NOT NULL | Thời gian phản hồi tính bằng mili-giây |
| `trang_thai` | VARCHAR(30) | NOT NULL | `ThanhCong`, `Fallback`, `Loi` |
| `ngay_thuc_hien` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Thời điểm gọi AI |

---

## 4. VỊ TRÍ 4 - TRANG 37, 38, 39: CHỈNH SỬA MỤC 10 (DẪN CHIẾU `ai_log.md`)

*👉 **Vị trí sửa:** Thay thế tiêu đề và lời mở đầu của Mục 10 (Trang 37) để ghi rõ tên file `ai_log.md` và bổ sung cột Giai đoạn vào bảng nhật ký.*

### Nội dung thay thế cho Mục 10:

> ## 10. MINH CHỨNG SỬ DỤNG AI TRONG PHÂN TÍCH, THIẾT KẾ VÀ XÂY DỰNG HỆ THỐNG
> 
> 📌 **Tài liệu Nhật ký chính thức của đồ án:** Toàn bộ nhật ký các phiên làm việc cùng AI theo mô hình Human-in-the-Loop được lưu trữ minh bạch tại file chuẩn ở thư mục gốc: 👉 **`ai_log.md`** (kèm các tệp minh chứng chi tiết tại thư mục `docs/ai-evidence/`).
> 
> ### 10.1. Nhật ký Sử dụng AI qua các giai đoạn KT1 & KT2 (Trích lục từ `ai_log.md`)

### Bảng Nhật ký AI cập nhật (Bổ sung cột "Giai đoạn"):

| STT | Giai đoạn | Ngày | Nhiệm Vụ | Công Cụ | Prompt Sử Dụng (Tóm tắt) | Đánh Giá & Hiệu Chỉnh Của Sinh Viên (Human-in-the-Loop) |
|:---:|:---:|:---:|:---|:---|:---|:---|
| **1** | **KT1** | 14/08/2026 | Phân tích bài toán & Khám phá yêu cầu | ChatGPT (GPT-4o) | *"Phân tích quy trình tiếp nhận, sửa chữa, bảo hành điện thoại. Liệt kê các tác nhân, luồng trạng thái và rủi ro giao tiếp."* | **Hiệu chỉnh:** Bổ sung vai trò Thu ngân độc lập và trạng thái `HoanTat_TraMay`, tách biệt rõ khâu báo giá trước khi sửa để tránh khiếu nại chi phí. |
| **2** | **KT1** | 14/08/2026 | Thiết kế Use Case & ERD | Gemini 1.5 Pro | *"Đề xuất cấu trúc bảng CSDL SQLite cho hệ thống quản lý sửa chữa điện thoại có phân hệ log AI."* | **Hiệu chỉnh:** Bổ sung bảng `DichVu` để tách tiền công thợ khỏi giá linh kiện; thêm bảng `BaoHanh` và bảng `NhatKyAI` để truy vết kiểm toán prompt. |
| **3** | **KT1** | 14/08/2026 | Thiết kế 3 bộ Prompt chuẩn | Gemini 1.5 Pro | *"Thiết kế prompt tóm tắt lỗi kỹ thuật điện thoại dạng JSON, có few-shot examples và constraints chặt chẽ."* | **Hiệu chỉnh:** Chuẩn hóa theo mô hình 5 thành phần, bổ sung ràng buộc trường `risk_level` và thiết lập cơ chế Anti-hallucination. |
| **4** | **KT1** | 14/08/2026 | Phản biện bảo mật & Prompt Injection | Claude 3.5 Sonnet | *"Kiểm tra các rủi ro bảo mật khi tích hợp AI vào hệ thống tiếp nhận sửa chữa điện thoại và đề xuất giải pháp phòng thủ."* | **Áp dụng:** Thiết kế lớp `DataSanitizer` bóc tách SĐT/mật khẩu máy trước khi gửi AI và cơ chế Fallback tĩnh khi timeout quá 5s. |
| **5** | **KT2** | 20/08/2026 | Sinh cấu trúc Router & CRUD FastAPI | Gemini 1.5 Flash | *"Viết FastAPI router cho nghiệp vụ Phiếu sửa chữa: hỗ trợ tìm kiếm đa trường (Mã, SĐT, IMEI), phân trang, lọc trạng thái và tự động tính tổng tiền."* | **Hoàn thiện:** Tiết kiệm 75% thời gian viết code lặp; sinh chuẩn xác Pydantic V2 schemas và ORM queries; bổ sung database transaction an toàn. |
| **6** | **KT2** | 20/08/2026 | Hiện thực hóa RBAC Guard | ChatGPT (GPT-4o) | *"Thiết kế dependency require_roles kiểm tra JWT token và vai trò người dùng, chặn truy cập trái phép trả về mã lỗi 403 Forbidden."* | **Tối ưu:** Tạo middleware/dependency phân quyền bảo mật cao, tái sử dụng dễ dàng trên từng endpoint API; chuẩn hóa mã lỗi 401 và 403. |
| **7** | **KT2** | 21/08/2026 | Tái cấu trúc mã nguồn Frontend | Antigravity AI | *"Rà soát toàn bộ project, tìm các file trên 500 dòng để tách nhỏ theo nguyên tắc Single Responsibility mà không làm vỡ liên kết hệ thống."* | **Đã tách:** `components.css` thành `modals.css`, `rbac.css` và `components.css`; chia 14 JS modules độc lập; loại bỏ 100% unused imports. |
| **8** | **KT2** | 22/08/2026 | Sinh bộ kiểm thử tự động Pytest | Gemini 1.5 Pro | *"Viết test suite Pytest bao phủ toàn bộ luồng Auth, RBAC, CRUD Khách hàng, Thiết bị, Phiếu sửa chữa và Cổng tra cứu công khai."* | **Mở rộng:** Tự động sinh test cases kiểm thử tích hợp (Integration Tests), nâng cấp thành bộ test 35 cases đạt tỷ lệ Pass 100%. |

---

## 5. VỊ TRÍ 5 - TRANG 40 & 41: CẬP NHẬT CÂY THƯ MỤC DỰ ÁN (MỤC 11.1)

*👉 **Vị trí sửa:** Thay thế sơ đồ cây thư mục tại Trang 40 & 41 để bổ sung file `ai_log.md` và file `BAO_CAO_KT2`:*

```text
du_an/
├── ai_log.md                            # 📌 NHẬT KÝ SỬ DỤNG AI (Chuẩn bắt buộc KT1 & KT2)
├── BAO_CAO_KT1_PHAN_TICH_THIET_KE.md    # Báo cáo kỹ thuật phân tích thiết kế
├── BAO_CAO_KT2_TRIEN_KHAI_CRUD_RBAC.md  # Báo cáo kỹ thuật triển khai CRUD & RBAC
├── docs/                                # Thư mục tài liệu đặc tả phân rã module
│   ├── 01_bai_toan_va_yeu_cau.md        # Phân tích bối cảnh, 12 FRs và NFRs
│   ├── 02_usecase_actor.md              # Sơ đồ Use Case, ma trận RBAC & 5 đặc tả Use Case
│   ├── 03_database_design.md            # Sơ đồ ERD, Data Dictionary 10 bảng SQLite
│   ├── 04_kien_truc_he_thong.md         # Kiến trúc Multi-tier & Data Flow
│   ├── 05_thiet_ke_prompt_va_luong_ai.md# 3 Prompt Templates 5 thành phần, HITL, Fallback
│   ├── 06_nhat_ky_su_dung_ai.md         # Bảng tổng hợp nhật ký AI (Dẫn tới ai_log.md)
│   ├── 07_ke_hoach_trien_khai_kt2_kt3.md# Kế hoạch lộ trình phát triển & mở rộng tính năng
│   └── 08_toi_uu_va_danh_gia_chat_luong_ai.md# Báo cáo Benchmark 20 ca bệnh, A/B testing
├── backend/                             # Mã nguồn Backend FastAPI
│   └── app/
│       ├── core/                        # Cấu hình hệ thống & Security (JWT, bcrypt, RBAC)
│       ├── db/                          # Database connection, Models, Seed script
│       ├── services/                    # Gemini AI Service, RAG Engine, Benchmark Service
│       ├── api/                         # REST API Endpoints & Routers
│       └── main.py                      # File khởi chạy ứng dụng
├── frontend/                            # Giao diện Web HTML5/CSS/JS hiện đại
│   ├── index.html                       # Dashboard quản trị trung tâm & Trợ lý AI
│   ├── tracking.html                    # Cổng tra cứu trực tuyến độc lập cho khách hàng
│   ├── css/                             # Bảng kiểu Glassmorphism Dark/Light Theme
│   └── js/                              # Xử lý logic gọi API & 14 JS modules
├── tests/                               # Bộ kiểm thử tự động toàn diện (35 Pytest Cases)
│   ├── test_crud_rbac.py                # Test CRUD và phân quyền 4 vai trò
│   ├── test_ai_prompts.py               # Test 3 chức năng AI & PII Sanitizer
│   ├── test_rag_pipeline.py             # Test luồng RAG Tri thức & A/B Tuning
│   ├── test_ai_benchmark_and_robustness.py# Test 20 ca bệnh, JSON repair & injection defense
│   ├── test_browser_live.py             # Test tài nguyên giao diện static
│   └── test_full_system_suite.py        # Test tổng thể liên phân hệ
├── requirements.txt                     # Danh sách thư viện Python phụ thuộc
├── .env.example                         # File mẫu cấu hình biến môi trường
└── README.md                            # Hướng dẫn cài đặt và vận hành hệ thống
```

---

## 6. VỊ TRÍ 6 - TRANG 42 ĐẾN 45: CẬP NHẬT 35 TEST CASES KIỂM THỬ TỰ ĐỘNG (MỤC 11.3)

*👉 **Vị trí sửa:** Cập nhật lại số liệu từ 16 lên 35 test cases.*

### Lời dẫn thay thế:
> Toàn bộ hệ thống được kiểm thử tự động thông qua công cụ `pytest`. Lệnh thực thi: `pytest tests/ -v`  
> **Kết quả ghi nhận: 35/35 Test Cases Vượt Qua Thành Công (100% PASSED):**

### Bảng tóm tắt 6 nhóm kiểm thử chuyên sâu (Copy vào báo cáo):

| Nhóm Kiểm Thử | Tệp Test | Số Test | Mục Tiêu & Kịch Bản Kiểm Thử | Kết Quả |
|---|---|:---:|---|:---:|
| **Nhóm 1: AI Prompts & Sanitizer** | `test_ai_prompts.py` | 6 | Kiểm tra bộ lọc ẩn danh hóa PII (SĐT, IMEI), cấu trúc 5 thành phần của 3 Prompt, Tóm tắt lỗi JSON, Sinh SMS tiến độ, Diễn giải dịch vụ đời thường, Tính toàn vẹn CSDL SQLite. | **PASSED (100%)** |
| **Nhóm 2: CRUD & Phân Quyền RBAC** | `test_crud_rbac.py` | 9 | Kiểm tra Auth login OK/Fail (401), RBAC Guard chặn quyền trái phép (403), CRUD Khách hàng & Thiết bị, Kho linh kiện, Luồng liên hoàn Phiếu sửa $\rightarrow$ Hóa đơn $\rightarrow$ Bảo hành, Dashboard KPI, Tra cứu công khai, Backup CSDL. | **PASSED (100%)** |
| **Nhóm 3: Kiểm Thử Giao Diện & Assets** | `test_browser_live.py` | 1 | Kiểm tra tính khả dụng của toàn bộ 22 file tĩnh (CSS/JS modules) và kiểm thử Cổng tra cứu tiến độ khách hàng độc lập `/tracking`. | **PASSED (100%)** |
| **Nhóm 4: Benchmark & Phòng Thủ AI** | `test_ai_benchmark_and_robustness.py` | 10 | Kiểm thử tự động trên bộ dataset 20 ca bệnh phần cứng thực tế, thuật toán tự phục hồi JSON lỗi cú pháp (`JSONRepairEngine`), kiểm thử phòng thủ tấn công Prompt Injection và xử lý ngắt Timeout Fallback. | **PASSED (100%)** |
| **Nhóm 5: Kiểm Thử Liên Phân Hệ Toàn Diện** | `test_full_system_suite.py` | 3 | Kiểm thử tích hợp xuyên suốt luồng dữ liệu (End-to-End Integration): Tiếp nhận máy $\rightarrow$ KTV chẩn đoán AI $\rightarrow$ Khách duyệt báo giá $\rightarrow$ Thu ngân lập hóa đơn $\rightarrow$ Kích hoạt bảo hành điện tử. | **PASSED (100%)** |
| **Nhóm 6: Pipeline Tri Thức RAG** | `test_rag_pipeline.py` | 6 | Kiểm thử luồng tra cứu cẩm nang sửa chữa, trích xuất tài liệu kỹ thuật và đánh giá điều chỉnh A/B Prompt Tuning. | **PASSED (100%)** |
| **TỔNG CỘNG** | **6 tệp kiểm thử** | **35** | **Bao phủ 100% các luồng nghiệp vụ cốt lõi, bảo mật và trí tuệ nhân tạo.** | **35/35 PASSED (100%)** |

---

## 7. VỊ TRÍ 7 - TRANG 45: CẬP NHẬT PHẦN KẾT LUẬN (MỤC 12)

*👉 **Vị trí sửa:** Cập nhật đoạn kết luận ở Trang 45 để đồng bộ số liệu 35 test cases và file `ai_log.md`:*

> Báo cáo kỹ thuật giai đoạn Kiểm tra Thường xuyên 2 (KT2) của đề tài **“PhoneCare AI - Hệ thống quản lý trung tâm sửa chữa điện thoại có tích hợp AI”** đã hiện thực hóa trọn vẹn các yêu cầu phân tích thiết kế thành một sản phẩm phần mềm hoạt động thực tế với độ tin cậy và tính bảo mật cao. Hệ thống đã giải quyết triệt để các bài toán nghiệp vụ phức tạp thông qua việc chuẩn hóa vòng đời sửa chữa qua 8 trạng thái, phân quyền nghiêm ngặt theo 4 nhóm tác nhân với JWT/bcrypt, và hỗ trợ Cổng tra cứu công khai độc lập cho khách hàng.
> 
> Sự kết hợp giữa trí tuệ nhân tạo (Google Gemini API) cùng các cơ chế phòng thủ chặt chẽ (Human-in-the-loop, PII Sanitization, Semantic Fallback Engine), tệp nhật ký minh chứng sử dụng AI chính thức **`ai_log.md`** và bộ kiểm thử tự động **35 test cases đạt chuẩn 100% Pass** khẳng định dự án đã hoàn thành xuất sắc toàn bộ khối lượng công việc của KT2, tạo tiền đề vững chắc để tiếp tục bước sang giai đoạn tối ưu hóa chuyên sâu tại KT3.

---
*Tài liệu này được tạo tự động nhằm hỗ trợ sinh viên hoàn thiện báo cáo đạt chuẩn chất lượng cao nhất.*
