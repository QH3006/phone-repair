# NHẬT KÝ THAY ĐỔI (CHANGELOG)
## Dự Án: Hệ Thống Quản Lý Trung Tâm Sửa Chữa Điện Thoại Tích Hợp AI (PhoneCare AI)

Toàn bộ các thay đổi, bổ sung tính năng, tối ưu hóa kiến trúc và sửa lỗi của dự án PhoneCare AI được ghi nhận chi tiết theo chuẩn [Keep a Changelog](https://keepachangelog.com/vi/1.0.0/) và tuân thủ nguyên tắc [Semantic Versioning](https://semver.org/).

---

## [v2.1.0] - 2026-09-04 (Hoàn Thiện Tính Năng KT2, Cổng Khách Hàng & Tinh Gọn Mã Nguồn)

Bản phát hành tập trung tối ưu hóa kiến trúc mã nguồn sạch, hoàn thiện các yêu cầu mở rộng thực tế cho giai đoạn KT2, giải quyết triệt để lỗi giao diện và bổ sung tiện ích khách hàng.

### 🚀 Thêm mới (Added)
* **Cổng Tra Cứu Khách Hàng Công Khai Độc Lập (`/tracking` & `/tra-cuu`):**
  - Xây dựng trang Landing Page riêng biệt `frontend/tracking.html` phục vụ khách hàng theo dõi tiến độ thời gian thực.
  - Tích hợp thanh tiến trình Timeline 8 bước sinh động, hiển thị chẩn đoán lỗi phần cứng và giải thích kỹ thuật bằng ngôn ngữ đời thường từ AI.
  - Không yêu cầu đăng nhập tài khoản, bảo vệ an toàn thông tin nội bộ.
* **API Tra Cứu Tiến Độ Công Khai:**
  - Bổ sung endpoint `GET /api/repairs/lookup?q=...` trong `repairs.py` hỗ trợ tìm kiếm theo Mã phiếu (`PSC-20260814-001`), Số điện thoại khách hàng hoặc Số IMEI thiết bị.
* **Tính Năng In Ấn Chứng Từ Chuẩn Khổ Giấy (FR-03 & FR-07):**
  - In phiếu biên nhận tiếp nhận máy (`printRepairReceipt`): đầy đủ logo trung tâm, thông tin khách hàng, hiện trạng máy, chi phí dự kiến, điều khoản bảo mật dữ liệu và chữ ký 2 bên.
  - In hóa đơn thanh toán dịch vụ (`printInvoice`): bóc tách chi phí linh kiện, tiền công kỹ thuật, mã hóa đơn và chữ ký kế toán/thu ngân.
* **Xuất Dữ Liệu Báo Cáo ra File CSV (FR-09):**
  - Chức năng xuất danh sách phiếu sửa chữa ra file `.csv` chuẩn UTF-8 có Byte Order Mark (BOM), tương thích hoàn hảo với Microsoft Excel mà không bị lỗi font tiếng Việt.
* **Script Tự Động Sao Lưu & Phục Hồi CSDL (NFR-08):**
  - File script độc lập `backup_db.py` áp dụng chuẩn SQLite Online Backup API an toàn, tạo các bản snapshot có gắn timestamp trong thư mục `backups/phone_repair_{timestamp}.bak`.
  - Hỗ trợ đầy đủ các tham số dòng lệnh: `--backup` (sao lưu), `--list` (liệt kê), `--restore <path>` (khôi phục an toàn).

### ⚡ Tối ưu hóa & Tái cấu trúc (Changed)
* **Kiểm soát độ dài file mã nguồn (< 500 dòng):**
  - Tách nhỏ file `frontend/css/components.css` (từ 659 dòng) thành 3 file CSS module hóa chuyên biệt:
    + `components.css`: Chứa các UI components dùng chung (Cards, Tables, Badges, Buttons, Forms).
    + `modals.css`: Chứa toàn bộ định dạng Modal Dialogs, backdrop blur và close buttons.
    + `rbac.css`: Chứa toàn bộ định dạng phân quyền RBAC, Role Switcher Banner và trạng thái khóa quyền.
  - Tách riêng module `frontend/js/modules/tracking-print.js` (283 dòng) và template `modal-tracking-print.html` (48 dòng), giữ 100% file code trong dự án dưới 450 dòng.
* **Tinh gọn Backend Router:**
  - Chuẩn hóa hàm helper `_serialize_repair_ticket()` trong `repairs.py`, loại bỏ hơn 50 dòng code mapping trùng lặp giữa `list_repairs` và `get_repair_detail`.
  - Dọn sạch 100% Unused Imports trên toàn bộ 10 file router và core modules backend.
* **Tối ưu CSS Layout Responsive:**
  - Cập nhật `.grid-2` sử dụng `grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)` và bổ sung breakpoint `@media (max-width: 1100px)` tự động chuyển thành cột đơn xếp chồng trên màn hình hẹp.
* **Cập nhật Bộ Kiểm Thử Tự Động:**
  - Nâng cấp test suite từ 14 lên **16/16 test cases Pytest PASSED 100%** (bổ sung `test_public_repair_lookup` và `test_database_backup_nfr08`).

### 🐛 Sửa lỗi (Fixed)
* **Khắc phục lỗi tràn lề phía bên phải (Clipped UI Layout):**
  - Sửa lỗi khối `<pre class="json-view">` làm phình to cột lưới CSS Grid; thêm thuộc tính tự ngắt dòng `white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere;`.
  - Thiết kế lại khối hiển thị kết quả AI Sandbox dạng Card tóm tắt có cấu trúc kèm khối xem JSON kỹ thuật thô dạng đóng/mở (`<details>`).
* **Khắc phục lỗi hiển thị `undefined` tại Lời tư vấn đời thường:**
  - Sửa lỗi lệch tên trường dữ liệu giữa backend (`message`) và frontend (`data.data.explanation`) trong tác vụ AI `GiaiThichDichVu`; backend hiện trả về đồng thời cả `message` và `explanation`.
* **Khắc phục sự cố nút "Khách tra cứu" không phản hồi:**
  - Bổ sung quy tắc kích hoạt hiển thị `.modal.active, .modal.show { display: flex !important; }` trong `modals.css` và đồng bộ `style.display = 'flex'` trong `tracking-print.js`.

---

## [v2.0.0] - 2026-08-21 (Hiện Thực Hóa CRUD Nghiệp Vụ & Phân Quyền RBAC - Giai Đoạn KT2)

Bản phát hành lớn chuyển giao toàn bộ kết quả phân tích thiết kế của KT1 thành mã nguồn ứng dụng web fullstack chạy thực tế.

### 🚀 Thêm mới (Added)
* **Hệ thống Xác thực & Phân quyền RBAC 4 Vai trò:**
  - Triển khai xác thực JWT Bearer token với thuật toán HS256, thời hạn sống 8 giờ.
  - Băm mật khẩu người dùng bằng thuật toán bảo mật `bcrypt` với muối an toàn.
  - Middleware bảo vệ Dependency `require_roles` kiểm soát phân quyền trên từng API endpoint cho 4 vai trò: `QuanLy`, `LeTan`, `KyThuatVien`, `ThuNgan`.
  - Thanh công cụ chuyển đổi vai trò trực quan (Role Switcher Banner) hỗ trợ kiểm tra phân quyền tức thì trên giao diện SPA.
* **Hiện thực hóa 100% CRUD các phân hệ nghiệp vụ:**
  - Phân hệ Người dùng & Nhân sự (`/api/users`): Thêm, sửa, khóa tài khoản và phân vai trò.
  - Phân hệ Khách hàng & Thiết bị (`/api/customers`, `/api/devices`): Quản lý quan hệ 1-N giữa khách hàng và các máy sửa chữa, tra cứu IMEI.
  - Phân hệ Kho Linh kiện & Bảng giá Dịch vụ (`/api/parts`, `/api/services`): Quản lý tồn kho, định mức tối thiểu, cảnh báo hết hàng và bảng giá công thợ.
  - Phân hệ Phiếu Sửa Chữa & Chi tiết (`/api/repairs`, `/api/repairs/{id}/items`): Quản lý vòng đời sửa chữa qua 8 trạng thái chuẩn hóa, tự động khấu trừ tồn kho linh kiện khi thêm vào phiếu.
  - Phân hệ Hóa đơn & Sổ Bảo hành Điện tử (`/api/invoices`, `/api/warranties`): Lập hóa đơn thu tiền, hỗ trợ tiền mặt và chuyển khoản; tự động kích hoạt cấp thẻ bảo hành điện tử theo hạn linh kiện.
  - Phân hệ Dashboard Thống kê Thời gian thực (`/api/stats/overview`): Tổng hợp KPI, doanh thu, phân bổ trạng thái và top lỗi máy phổ biến.
* **Giao diện Web Single Page Application (SPA):**
  - 9 Tab nghiệp vụ tương tác mượt mà không tải lại trang: Dashboard, Phiếu sửa chữa, Khách hàng, Kho linh kiện, Hóa đơn & Bảo hành, Nhân sự & RBAC, AI Copilot, Nhật ký Audit Logs, Kiến trúc & Use Case.
  - Hỗ trợ chuyển đổi giao diện Sáng / Tối (Dark/Light Mode) lưu trạng thái qua `localStorage`.
* **Bộ Kiểm Thử Tự Động Ban Đầu:**
  - Xây dựng 14 test cases tự động kiểm tra xác thực, RBAC, CRUD, AI prompts và dữ liệu mẫu Seed Data.

### 🔒 Bảo mật (Security)
* Triển khai bộ làm sạch dữ liệu PII (`DataSanitizer`) tự động bóc tách và ẩn danh hóa Số điện thoại, IMEI và Mật khẩu máy trước khi gửi payload tới Google Gemini API.
* Thiết lập biến môi trường bảo mật qua `.env`, loại bỏ hoàn toàn việc hardcode API key hoặc JWT secret trong mã nguồn.

---

## [v1.0.0] - 2026-08-14 (Phân Tích & Thiết Kế Hệ Thống - Giai Đoạn KT1)

Bản phát hành đầu tiên hoàn thành toàn diện 10 tiêu chí đánh giá phân tích thiết kế kỹ thuật phần mềm hướng AI.

### 🚀 Thêm mới (Added)
* **Khảo sát bài toán & Quy trình nghiệp vụ:**
  - Phân tích bối cảnh trung tâm dịch vụ sửa chữa điện thoại di động (30 - 80 ca/ngày, đội ngũ 8 - 12 nhân sự).
  - Xác định 4 điểm nghẽn thực tế (Pain points) trong quy trình truyền thống As-Is và đề xuất giải pháp To-Be tích hợp AI.
* **Đặc tả yêu cầu chức năng & phi chức năng:**
  - Xác định đầy đủ 12 yêu cầu chức năng (`FR-01` đến `FR-12`).
  - Lập bảng đặc tả 10 yêu cầu phi chức năng (`NFR-01` đến `NFR-10`) theo chuẩn bảng 7 cột thuộc 6 nhóm kỹ thuật.
* **Thiết kế Actor & Use Case:**
  - Xây dựng sơ đồ Use Case tổng quát và ma trận phân quyền RBAC.
  - Đặc tả chi tiết 5 ca sử dụng trọng tâm: Tiếp nhận máy (UC-03), Chẩn đoán kỹ thuật (UC-05), Lập hóa đơn (UC-07), AI Tóm tắt lỗi (UC-10), AI Sinh tin nhắn tiến độ (UC-11).
* **Thiết kế Cơ sở dữ liệu quan hệ (ERD):**
  - Thiết kế sơ đồ quan hệ thực thể ERD chuẩn hóa gồm 9 thực thể dữ liệu quan hệ.
  - Xây dựng Từ điển dữ liệu chi tiết (Data Dictionary) cho 9 bảng.
* **Thiết kế Kiến trúc hệ thống:**
  - Mô hình kiến trúc đa tầng (Multi-tier Architecture with AI Integration): Client SPA $\rightarrow$ FastAPI Gateway $\rightarrow$ SQLAlchemy ORM $\rightarrow$ SQLite CSDL $\rightarrow$ Cloud Gemini API.
* **Thiết kế 3 Bộ Prompt AI Chuẩn 5 Thành Phần:**
  - Prompt 1 (FR-10): Chuyển đổi ghi chú kỹ thuật thô của KTV thành cấu trúc JSON chuẩn gồm 4 trường.
  - Prompt 2 (FR-11): Tự động sinh tin nhắn SMS/Zalo cập nhật tiến độ cho khách hàng.
  - Prompt 3 (FR-12): Diễn giải bản chất hư hỏng bằng hình ảnh ẩn dụ đời thường (Metaphor).
* **Nguyên tắc quản trị rủi ro AI:**
  - Thiết lập cơ chế con người phê duyệt (Human-in-the-loop - HITL).
  - Cơ chế phòng thủ ngữ nghĩa cục bộ (Rule-based Semantic Fallback Engine) khi mất mạng hoặc API timeout quá 5.0s.
