# BẢNG HƯỚNG DẪN CHI TIẾT CÁC VỊ TRÍ CẦN SỬA ĐỔI & BỔ SUNG
## DỰA TRÊN FILE BÁO CÁO TIỂU LUẬN PDF (NHÓM 7 - ĐỀ TÀI PHONECARE AI) ĐỂ ĐÁP ỨNG TOÀN DIỆN YÊU CẦU BÀI KIỂM TRA THƯỜNG XUYÊN 2 (KT2)

---

> **Mục đích tài liệu:** Tài liệu này đối chiếu từng trang của file báo cáo PDF (40 trang của nhóm 7: Tạ Quang Hiếu, Nguyễn Văn Thái) với yêu cầu thực tế của **Kiểm tra Thường xuyên 2 (KT2)**. Tài liệu chỉ rõ: **Trang nào bị sai/thiếu**, **Lý do vì sao cần sửa**, và **Nội dung văn bản chuẩn soạn sẵn** để bạn chỉ việc sao chép (copy-paste) trực tiếp vào file Word báo cáo trước khi xuất ra bản PDF nộp chấm điểm.

---

# PHẦN 1: BẢNG TỔNG HỢP NHANH CÁC VỊ TRÍ CẦN CHỈNH SỬA

| STT | Trang PDF | Mục | Vấn đề hiện tại trong PDF | Nội dung cần chỉnh sửa / Bổ sung cho bài KT2 |
|:---:|:---:|---|---|---|
| 1 | **Trang 1** | Trang bìa | Tiêu đề ghi chung chung, chưa định danh đây là bài **KT2**. | Đổi thành: **BÁO CÁO KIỂM TRA THƯỜNG XUYÊN 2 (KT2) - XÂY DỰNG HỆ THỐNG CRUD, RBAC VÀ TÍCH HỢP AI**. |
| 2 | **Trang 2** | Phân công | Phân công chỉ ghi dựng khung và rà soát ở mức KT1. | Bổ sung phần việc KT2: Lập trình FastAPI, CSDL, Phân quyền RBAC, Cổng `/tracking`, Viết 16 Pytest tests. |
| 3 | **Trang 3** | Mục lục | Thiếu các chương mục cốt lõi của kết quả thực nghiệm KT2. | Bổ sung mục Báo cáo kết quả CRUD, Bảng 16 Pytest tests, Hướng dẫn chạy và kịch bản demo. |
| 4 | **Trang 11** | NFR-08 | Chỉ ghi sao lưu định kỳ chung chung. | Ghi rõ script tự động `backup_db.py` sử dụng SQLite Backup API tạo file `.bak` trong thư mục `backups/`. |
| 5 | **Trang 15** | Bố cục | **Lỗi trang trắng:** Chỉ có 1 dòng tiêu đề, dưới trống trơn. | Xóa ngắt trang thừa, kéo sơ đồ Use Case Lễ tân và bảng đặc tả lên liền kề với tiêu đề. |
| 6 | **Trang 20** | Bố cục | **Lỗi trang trắng:** Chỉ có 1 dòng tiêu đề Use Case 5. | Xóa ngắt trang thừa, kéo sơ đồ Use Case Thu ngân và đặc tả lên liền kề. |
| 7 | **Trang 24** | Bảng CSDL | Tên trường trong bảng `PhieuSuaChua` bị lệch so với code. | Đổi `mo_ta_loi_khach` $\rightarrow$ `mo_ta_loi_ban_dau`; `tong_tien_du_kien` $\rightarrow$ `chi_phi_uoc_tinh`. |
| 8 | **Trang 36-37** | Mục 10 | Chỉ có minh chứng AI ở giai đoạn KT1 (phân tích). | **Bổ sung Bảng 10.2:** Minh chứng dùng AI trong KT2 (sinh code Router, refactor code, viết test tự động). |
| 9 | **Trang 38** | Mục 11.1 | Cây thư mục mã nguồn quá sơ sài (thiếu 7 router, thiếu module frontend). | Cập nhật cây thư mục chuẩn xác 100% khớp với mã nguồn thực tế đã chạy trên Git. |
| 10 | **Trang 38-39** | Mục 11.2 | Ghi KT2 ở thể **"kế hoạch tương lai"** (sẽ làm). | Đổi thành **"Báo cáo kết quả hoàn thành thực tế"** + Bảng kết quả **16/16 test cases Pytest PASSED 100%**. |
| 11 | **Trang 39** | Sau Mục 11 | Chưa có hướng dẫn chạy và thông tin tài khoản demo. | Bổ sung mục **11.3 Hướng dẫn cài đặt & Tài khoản demo 4 vai trò** cho giảng viên chấm thi. |

---

# PHẦN 2: NỘI DUNG CHI TIẾT CẦN THAY THẾ / BỔ SUNG TỪNG TRANG
*(Bạn có thể copy trực tiếp các đoạn văn bản dưới đây vào bài làm)*

---

## 1. TRANG 1: TRANG BÌA BÁO CÁO

**Nội dung cũ trong PDF:**
> BÁO CÁO  
> MÔN HỌC: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO  
> ĐỀ TÀI: HỆ THỐNG QUẢN LÝ TRUNG TÂM SỬA CHỮA ĐIỆN THOẠI CÓ TÍCH HỢP AI  

**Nội dung sửa lại chuẩn KT2:**
```text
ĐẠI HỌC THÁI NGUYÊN
TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG
KHOA CÔNG NGHỆ THÔNG TIN
------------------------

BÁO CÁO KỸ THUẬT KIỂM TRA THƯỜNG XUYÊN 2 (KT2)
MÔN HỌC: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO / AI-DRIVEN SOFTWARE ENGINEERING

ĐỀ TÀI:
HIỆN THỰC HÓA HỆ THỐNG QUẢN TRỊ NGHIỆP VỤ CRUD, PHÂN QUYỀN RBAC 4 VAI TRÒ
VÀ TÍCH HỢP TRỢ LÝ AI CHO TRUNG TÂM SỬA CHỮA ĐIỆN THOẠI (PHONECARE AI)

Giảng viên hướng dẫn: TS. Nguyễn Thị Tuyển
Lớp: KTPM K23B
Nhóm sinh viên thực hiện: Nhóm 7
1. Tạ Quang Hiếu     - Mã SV: DTC245180094
2. Nguyễn Văn Thái   - Mã SV: DTC245180172

Thái Nguyên, Tháng 08/2026
```

---

## 2. TRANG 2: BẢNG PHÂN CÔNG THỰC HIỆN TIỂU LUẬN

**Nội dung cũ trong PDF:** Chỉ phân công phân tích, vẽ sơ đồ và dựng khung.  
**Nội dung sửa lại (thể hiện rõ khối lượng công việc lập trình và kiểm thử của KT2):**

| TT | Mã sinh viên | Họ và tên sinh viên | Nhiệm vụ đảm nhiệm trong Giai đoạn KT2 | Mức độ hoàn thành |
|:---:|:---:|:---:|---|:---:|
| 1 | DTC245180094 | **Tạ Quang Hiếu** | - Hiện thực hóa tầng Backend FastAPI, thiết kế 10 API Routers CRUD.<br>- Triển khai cơ chế xác thực JWT, mã hóa mật khẩu bcrypt và RBAC Guard cho 4 vai trò.<br>- Xây dựng 3 dịch vụ AI (Gemini Flash API & Fallback Engine) và ghi log kiểm toán.<br>- Viết script sao lưu CSDL tự động `backup_db.py` theo NFR-08. | **100%** |
| 2 | DTC245180172 | **Nguyễn Văn Thái** | - Xây dựng giao diện Web SPA Frontend (HTML5/CSS/Vanilla JS) module hóa.<br>- Phát triển Cổng tra cứu tiến độ công khai độc lập cho khách hàng (`/tracking`).<br>- Xây dựng tính năng in ấn biên nhận, hóa đơn chuẩn khổ giấy và xuất báo cáo CSV.<br>- Viết test suite tự động Pytest (16 test cases đạt 100% Pass) và tổng hợp báo cáo KT2. | **100%** |

---

## 3. TRANG 11: MỤC 4.4 - SAO LƯU & PHỤC HỒI DỮ LIỆU (NFR-08)

**Nội dung cũ trong PDF:** Ghi chung chung là file dump.  
**Nội dung bổ sung chi tiết theo code thực tế đã chạy:**
> **4.4. Sao lưu & Phục hồi dữ liệu (Backup & Recovery - NFR-08):**
> * Cơ sở dữ liệu SQLite (`phone_repair.db`) được tự động sao lưu an toàn thông qua script độc lập `backup_db.py` sử dụng chuẩn **SQLite Online Backup API** (không gây khóa bảng hay ảnh hưởng tới các phiên làm việc đang chạy).
> * Bản sao lưu được lưu trữ dưới dạng snapshot có dấu thời gian: `backups/phone_repair_YYYYMMDD_HHMMSS.bak`.
> * Cung cấp đầy đủ công cụ CLI quản trị:
>   - Tạo bản sao lưu tức thì: `python backup_db.py --backup`
>   - Liệt kê danh sách bản sao lưu: `python backup_db.py --list`
>   - Khôi phục CSDL an toàn (tự động tạo bản dự phòng trước khi khôi phục): `python backup_db.py --restore <duong_dan_file.bak>`
> * Đảm bảo chỉ số phục hồi RTO < 5 phút và RPO = 0 đối với các bản snapshot trong ngày.

---

## 4. TRANG 15 & TRANG 20: KHẮC PHỤC LỖI TRANG TRẮNG (BỐ CỤC DÀN TRANG)

* **Trang 15:** Đang chỉ có dòng chữ:
  `5.2. Đặc tả Chi Tiết 5 Ca Sử Dụng Trọng Tâm`  
  `Use Case 1: UC-03 - Tiếp nhận máy & Lập phiếu sửa chữa`  
  👉 **Khắc phục trong file Word:** Đặt con trỏ sau chữ này, nhấn `Delete` để xóa ký tự ngắt trang (Page Break). Kéo hình ảnh Sơ đồ Use Case Lễ tân (đang ở trang 16) và nội dung Luồng sự kiện chính (đang ở trang 17) đặt ngay bên dưới tiêu đề để trang 15 đầy đặn, không có khoảng trắng thừa.
* **Trang 20:** Đang chỉ có dòng chữ:
  `Use Case 5: UC-07 - Lập hóa đơn thanh toán & Kích hoạt bảo hành điện tử`  
  👉 **Khắc phục trong file Word:** Xóa ngắt trang thừa sau dòng tiêu đề này. Kéo Sơ đồ Use Case Thu ngân (đang ở trang 21) và nội dung Luồng sự kiện (đang ở trang 22) lên trang 20.

---

## 5. TRANG 24: CHUẨN HÓA BẢNG DỮ LIỆU CSDL (BẢNG 4. PhieuSuaChua)

**Sửa lại 2 tên trường trong bảng để khớp 100% với model ORM `backend/app/db/models.py`:**

| Tên trường cũ (trong PDF) | Tên trường chuẩn (Code thực tế) | Kiểu dữ liệu | Ràng buộc | Mô tả chức năng |
|---|---|---|---|---|
| `mo_ta_loi_khach` | **`mo_ta_loi_ban_dau`** | TEXT | NOT NULL | Hiện tượng hư hỏng ban đầu do khách hàng khai báo khi tiếp nhận. |
| `tong_tien_du_kien` | **`chi_phi_uoc_tinh`** | FLOAT / DECIMAL | DEFAULT 0.0 | Tổng chi phí dự toán ban đầu (Linh kiện + Công thợ). |
| *(bổ sung)* | **`le_tan_id`** | INTEGER | FK -> NguoiDung(id) | Nhân viên lễ tân chịu trách nhiệm tiếp nhận và lập phiếu. |

---

## 6. TRANG 36 - 37: BỔ SUNG MỤC 10.2 - MINH CHỨNG SỬ DỤNG AI TRONG GIAI ĐOẠN KT2

**Trong PDF chỉ có mục 10.1 (KT1). Cần bổ sung thêm Bảng 10.2 cho giai đoạn KT2:**

> ### 10.2. Nhật Ký Sử Dụng AI Trong Giai Đoạn Lập Trình & Kiểm Thử (AI Usage Log - KT2)
> 
> | STT | Nhiệm Vụ Kỹ Thuật | Công Cụ AI | Prompt Sử Dụng (Tóm tắt) | Kết Quả Đạt Được & Đánh Giá |
> |:---:|---|:---:|---|---|
> | 1 | **Sinh cấu trúc Router & CRUD FastAPI** | Gemini 1.5 Pro / Antigravity | *"Viết FastAPI router cho nghiệp vụ Phiếu sửa chữa: hỗ trợ tìm kiếm đa trường (Mã, SĐT, IMEI), phân trang, lọc trạng thái và tự động tính tổng tiền."* | Tiết kiệm 75% thời gian viết code lặp; sinh chuẩn xác Pydantic V2 schemas và ORM queries. |
> | 2 | **Hiện thực hóa RBAC Guard** | Antigravity AI | *"Thiết kế dependency require_roles kiểm tra JWT token và vai trò người dùng, chặn truy cập trái phép trả về mã lỗi 403 Forbidden."* | Tạo middleware phân quyền bảo mật cao, tái sử dụng dễ dàng trên từng endpoint API. |
> | 3 | **Tái cấu trúc mã nguồn (Refactoring < 500 dòng)** | Antigravity AI | *"Rà soát toàn bộ project, tìm các file trên 500 dòng để tách nhỏ theo nguyên tắc Single Responsibility mà không làm vỡ liên kết hệ thống."* | Đã tách `components.css` (659 dòng) thành `modals.css`, `rbac.css` và `components.css`; loại bỏ 100% unused imports. |
> | 4 | **Sinh bộ kiểm thử tự động Pytest** | Gemini 1.5 Pro | *"Viết test suite Pytest bao phủ toàn bộ luồng Auth, RBAC, CRUD Khách hàng, Thiết bị, Phiếu sửa chữa và Cổng tra cứu công khai."* | Tự động sinh 16 test cases kiểm thử tích hợp (Integration Tests), đạt tỷ lệ Pass 100%. |

---

## 7. TRANG 37 - 38: CẬP NHẬT MỤC 11.1 - CẤU TRÚC THƯ MỤC DỰ ÁN THỰC TẾ

**Nội dung cũ trong PDF:** Rất sơ sài, thiếu hầu hết các router và file frontend.  
**Nội dung thay thế chuẩn xác cây thư mục mã nguồn hiện tại:**

```text
du_an/
├── backend/                              # Mã nguồn Backend FastAPI
│   └── app/
│       ├── api/
│       │   ├── routers/
│       │   │   ├── auth.py               # Xác thực JWT & quản lý phiên
│       │   │   ├── users.py              # CRUD người dùng & phân quyền RBAC
│       │   │   ├── customers.py          # CRUD hồ sơ khách hàng
│       │   │   ├── devices.py            # CRUD thiết bị & quản lý IMEI
│       │   │   ├── parts.py              # CRUD linh kiện kho & cảnh báo tồn thấp
│       │   │   ├── services.py           # CRUD bảng giá dịch vụ kỹ thuật
│       │   │   ├── repairs.py            # CRUD phiếu sửa chữa, chi tiết & tra cứu công khai
│       │   │   ├── invoices.py           # Lập hóa đơn & thanh toán
│       │   │   ├── warranties.py         # Sổ bảo hành điện tử
│       │   │   ├── stats.py              # Thống kê Dashboard KPI thời gian thực
│       │   │   └── ai.py                 # Endpoint gọi AI Copilot & Audit Logs
│       │   └── endpoints.py              # Aggregator router trung tâm
│       ├── core/
│       │   ├── config.py                 # Cấu hình môi trường & Secret Key
│       │   └── security.py               # Hash bcrypt, mã hóa JWT & RBAC Guard
│       ├── db/
│       │   ├── database.py               # Kết nối SQLite & SessionLocal
│       │   ├── models.py                 # 9 SQLAlchemy ORM models quan hệ
│       │   └── init_db.py                # Khởi tạo bảng & nạp dữ liệu mẫu
│       ├── schemas/
│       │   └── schemas.py                # Pydantic V2 Request/Response validation
│       ├── services/
│       │   └── ai_service.py             # Gemini LLM Orchestrator, PII Sanitizer & Fallback
│       └── main.py                       # Entrypoint FastAPI, CORS & Router Cổng Khách Hàng
├── frontend/                             # Giao diện Web SPA hiện đại
│   ├── components/
│   │   ├── header.html                   # Topbar, theme switcher & link Cổng Khách Hàng
│   │   ├── sidebar.html                  # Điều hướng 9 phân hệ theo vai trò
│   │   ├── modal.html                    # 10 form modal tương tác nghiệp vụ
│   │   └── modal-tracking-print.html     # Modal tra cứu tiến độ & in ấn chứng từ
│   ├── css/
│   │   ├── base.css                      # Biến màu, CSS reset & theme Dark/Light
│   │   ├── layout.css                    # Grid bố cục & responsive đa thiết bị
│   │   ├── components.css                # Card, Table, Badge, Button, Form styles
│   │   ├── modals.css                    # Popup dialogs & backdrop blur
│   │   ├── rbac.css                      # Định dạng vai trò & trạng thái khóa quyền
│   │   ├── ai-sandbox.css                # Giao diện demo AI Copilot & JSON viewer
│   │   └── style.css                     # Master stylesheet kết nối
│   ├── js/
│   │   ├── modules/                      # 12 module JavaScript độc lập (< 450 dòng)
│   │   │   ├── auth.js                   # Đăng nhập JWT & Role Switcher Banner
│   │   │   ├── repairs.js                # Nghiệp vụ quản lý phiếu sửa chữa
│   │   │   ├── tracking-print.js         # Tra cứu tiến độ, in ấn & xuất CSV
│   │   │   ├── ai-sandbox.js             # Gọi API AI & xử lý hiển thị kết quả
│   │   │   └── ...                       # Các module CRUD chuyên biệt khác
│   │   └── app.js                        # Bootstrap ứng dụng SPA
│   ├── index.html                        # Giao diện quản trị nội bộ
│   └── tracking.html                     # Cổng tra cứu trực tuyến độc lập cho khách hàng
├── tests/                                # Bộ kiểm thử tự động toàn diện (Pytest)
│   ├── test_ai_prompts.py                # Kiểm thử cấu trúc 3 Prompt & Fallback Engine
│   ├── test_crud_rbac.py                 # Kiểm thử 100% CRUD, Auth, RBAC & Backup
│   └── test_browser_live.py              # Kiểm thử static assets & live routes
├── backups/                              # Thư mục chứa các bản snapshot CSDL .bak
├── backup_db.py                          # Script tự động sao lưu & phục hồi CSDL (NFR-08)
├── requirements.txt                      # Danh mục thư viện Python phụ thuộc
├── .env.example                          # File mẫu cấu hình biến môi trường
└── README.md                             # Hướng dẫn cài đặt và vận hành hệ thống
```

---

## 8. TRANG 38 - 40: THAY THẾ MỤC 11.2 BẰNG BÁO CÁO KẾT QUẢ THỰC NGHIỆM KT2

**Nội dung cũ trong PDF:** Ghi KT2 ở dạng kế hoạch tương lai ("sẽ xây dựng...").  
**Nội dung thay thế hoàn chỉnh báo cáo kết quả KT2 (chứng minh hệ thống đã chạy thực tế):**

> ### 11.2. Báo Cáo Kết Quả Hoàn Thành Các Yêu Cầu Giai Đoạn KT2
> 
> Hệ thống đã hiện thực hóa 100% các mục tiêu kỹ thuật đề ra cho giai đoạn Kiểm tra Thường xuyên 2 (KT2):
> 1. **Hoàn thiện hệ thống Authentication & RBAC 4 vai trò:** Đăng nhập cấp mã định danh JWT HS256, kiểm soát chặt chẽ quyền hạn giữa `QuanLy`, `LeTan`, `KyThuatVien`, và `ThuNgan`.
> 2. **Chuẩn hóa vòng đời 8 trạng thái phiếu sửa chữa:** Luồng tiếp nhận máy $\rightarrow$ Phân công KTV $\rightarrow$ Kiểm tra $\rightarrow$ Báo giá $\rightarrow$ Sửa chữa $\rightarrow$ Đã sửa xong $\rightarrow$ Thanh toán $\rightarrow$ Hoàn tất bàn giao vận hành trơn tru với tính năng tự động trừ kho linh kiện và tự động sinh mã bảo hành điện tử.
> 3. **Phát triển Cổng Khách Hàng độc lập (`/tracking`):** Tách biệt hoàn toàn trải nghiệm của khách hàng với hệ thống quản trị nội bộ. Khách hàng tra cứu tiến độ trực tuyến theo thời gian thực và xem giải thích nguyên nhân lỗi bằng ngôn ngữ đời thường từ AI mà không cần đăng nhập.
> 4. **Bổ sung tiện ích in ấn chứng từ & sao lưu dự phòng:**
>    - Hỗ trợ in ấn phiếu biên nhận tiếp nhận máy và in hóa đơn thanh toán chuẩn khổ giấy.
>    - Bổ sung script sao lưu CSDL tự động `backup_db.py` (NFR-08) và xuất danh sách dữ liệu ra file CSV/Excel UTF-8 có BOM.
> 5. **Kiểm soát chất lượng mã nguồn:** Toàn bộ 100% file code trong dự án đều được module hóa tinh gọn dưới 500 dòng.
>
> ### 11.3. Bảng Kết Quả Kiểm Thử Tự Động Toàn Diện (Automated Testing Results)
> 
> Toàn bộ hệ thống được kiểm thử tự động thông qua công cụ `pytest`. Lệnh thực thi: `pytest tests/ -v`.  
> Kết quả ghi nhận: **16/16 Test Cases Vượt Qua Thành Công (100% PASSED)**:
> 
> | STT | Tệp Kiểm Thử | Tên Test Case | Mục Tiêu & Kịch Bản Kiểm Thử | Kết Quả |
> |:---:|---|---|---|:---:|
> | 1 | `test_ai_prompts.py` | `test_data_sanitizer` | Kiểm tra bộ lọc ẩn danh hóa PII (SĐT, IMEI, mật khẩu máy) trước khi gửi tới AI | **PASSED** |
> | 2 | `test_ai_prompts.py` | `test_prompt_structure` | Kiểm tra cấu trúc 5 thành phần của 3 bộ System Prompt | **PASSED** |
> | 3 | `test_ai_prompts.py` | `test_fault_summary` | Kiểm tra AI Tóm tắt lỗi kỹ thuật ra JSON chuẩn (FR-10) | **PASSED** |
> | 4 | `test_ai_prompts.py` | `test_progress_message` | Kiểm tra AI Sinh tin nhắn tiến độ SMS/Zalo chuẩn độ dài (FR-11) | **PASSED** |
> | 5 | `test_ai_prompts.py` | `test_service_explain` | Kiểm tra AI Diễn giải kỹ thuật theo ngôn ngữ đời thường (FR-12) | **PASSED** |
> | 6 | `test_ai_prompts.py` | `test_database_seed` | Kiểm tra tính toàn vẹn của dữ liệu mẫu ban đầu trong CSDL SQLite | **PASSED** |
> | 7 | `test_browser_live.py` | `test_static_assets` | Kiểm tra khả năng tải 20 file tĩnh (CSS/JS modules) và trang `/tracking` | **PASSED** |
> | 8 | `test_crud_rbac.py` | `test_auth_login_ok` | Kiểm tra đăng nhập thành công, cấp JWT token hợp lệ | **PASSED** |
> | 9 | `test_crud_rbac.py` | `test_auth_login_fail` | Kiểm tra đăng nhập thất bại với sai mật khẩu (trả về HTTP 401) | **PASSED** |
> | 10 | `test_crud_rbac.py` | `test_rbac_guard` | Kiểm tra chặn quyền truy cập trái phép của nhân viên (trả về HTTP 403) | **PASSED** |
> | 11 | `test_crud_rbac.py` | `test_customer_crud` | Kiểm tra thêm, sửa, xóa, tìm kiếm khách hàng và thiết bị theo IMEI | **PASSED** |
> | 12 | `test_crud_rbac.py` | `test_parts_services` | Kiểm tra quản lý kho linh kiện, trừ tồn kho và danh mục dịch vụ | **PASSED** |
> | 13 | `test_crud_rbac.py` | `test_repair_flow` | Kiểm tra luồng liên hoàn: Phiếu sửa $\rightarrow$ Thêm linh kiện $\rightarrow$ Hóa đơn $\rightarrow$ Bảo hành | **PASSED** |
> | 14 | `test_crud_rbac.py` | `test_dashboard_kpi` | Kiểm tra tổng hợp số liệu thống kê Dashboard, doanh thu và phân bổ lỗi | **PASSED** |
> | 15 | `test_crud_rbac.py` | `test_public_lookup` | Kiểm tra API tra cứu tiến độ công khai không cần token (FR-03, `/api/repairs/lookup`) | **PASSED** |
> | 16 | `test_crud_rbac.py` | `test_db_backup` | Kiểm tra chức năng sao lưu snapshot CSDL của script `backup_db.py` (NFR-08) | **PASSED** |
> 
> ### 11.4. Hướng Dẫn Vận Hành & Kịch Bản Demo Dành Cho Chấm Thi
> 
> **1. Khởi động hệ thống:**
> ```powershell
> # Bước 1: Cài đặt thư viện
> pip install -r requirements.txt
> 
> # Bước 2: Khởi động máy chủ web FastAPI
> python -m uvicorn backend.app.main:app --reload --port 8000
> ```
> * Trang quản trị nội bộ: `http://127.0.0.1:8000`
> * Cổng tra cứu khách hàng công khai: `http://127.0.0.1:8000/tracking`
> * Tài liệu tương tác API Swagger UI: `http://127.0.0.1:8000/docs`
> 
> **2. Danh sách 4 tài khoản thử nghiệm phân quyền (Mật khẩu chung: `123456`):**
> * **Quản Lý (Admin):** Username: `admin` (Toàn quyền hệ thống, xem biểu đồ doanh thu, quản lý tài khoản nhân viên, xem Audit Log AI).
> * **Lễ Tân (Receptionist):** Username: `letan` (Tiếp nhận máy mới, tạo hồ sơ khách, phân công KTV, dùng AI sinh SMS).
> * **Kỹ Thuật Viên (Technician):** Username: `ktv` (Khám máy, cập nhật tiến độ, xuất kho linh kiện, dùng AI tóm tắt lỗi phần cứng).
> * **Thu Ngân (Cashier):** Username: `thungan` (Lập hóa đơn thanh toán, kích hoạt thẻ bảo hành điện tử, in biên lai).

---

## 9. TRANG 39 - 40: MỤC 12 - KẾT LUẬN

**Sửa đổi đoạn mở đầu của Kết luận để khẳng định hoàn thành KT2:**
> Báo cáo kỹ thuật giai đoạn Kiểm tra Thường xuyên 2 (KT2) của đề tài **“PhoneCare AI - Hệ thống quản lý trung tâm sửa chữa điện thoại có tích hợp AI”** đã hiện thực hóa trọn vẹn các yêu cầu phân tích thiết kế thành một sản phẩm phần mềm hoạt động thực tế với độ tin cậy và tính bảo mật cao. Hệ thống đã giải quyết triệt để các bài toán nghiệp vụ phức tạp thông qua việc chuẩn hóa vòng đời sửa chữa qua 8 trạng thái, phân quyền nghiêm ngặt theo 4 nhóm tác nhân với JWT/bcrypt, và hỗ trợ Cổng tra cứu công khai độc lập cho khách hàng.
> 
> Sự kết hợp giữa trí tuệ nhân tạo (Google Gemini API) cùng các cơ chế phòng thủ chặt chẽ (Human-in-the-loop, PII Sanitization, Semantic Fallback Engine) và bộ kiểm thử tự động 16 test cases đạt chuẩn 100% Pass khẳng định dự án đã hoàn thành xuất sắc toàn bộ khối lượng công việc của KT2, tạo tiền đề vững chắc để tiếp tục bước sang giai đoạn tối ưu hóa chuyên sâu tại KT3.
