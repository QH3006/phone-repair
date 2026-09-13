# NHẬT KÝ THAY ĐỔI (CHANGELOG)
## Dự Án: Hệ Thống Quản Lý Trung Tâm Sửa Chữa Điện Thoại Tích Hợp AI (PhoneCare AI)

Toàn bộ các thay đổi, bổ sung tính năng, tối ưu hóa kiến trúc và sửa lỗi của dự án PhoneCare AI được ghi nhận chi tiết theo chuẩn [Keep a Changelog](https://keepachangelog.com/vi/1.0.0/) và tuân thủ nguyên tắc [Semantic Versioning](https://semver.org/).

---

## [v2.5.1] - 2026-09-14 (Hoàn Thiện Quản Lý Khách Hàng & Mật Khẩu Vẽ Hình Pattern Lock)

Bản cập nhật tối ưu hóa trải nghiệm thực tế tại quầy tiếp nhận thiết bị, xử lý tương thích mật khẩu bảo mật smartphone đa dạng.

### 🚀 Tính năng mới & Cải tiến (Added & Changed)
* **Hỗ Trợ Mật Khẩu Vẽ Mẫu Hình (Pattern Lock 9 Điểm):**
  - Tự động nhận diện và phân loại mật khẩu màn hình: Dạng vẽ hình (Pattern Lock), Mã số PIN, hoặc Không đặt khóa.
  - Hiển thị badge màu sắc trực quan: Badge tím sang trọng kèm icon ma trận 9 điểm cho dạng vẽ hình (ví dụ: `Vẽ hình: Chữ Z (1-2-3-5-7-8-9)`, `Vẽ hình: Chữ L`), Badge vàng cho mã PIN, Badge xám cho thiết bị không khóa.
  - Bổ sung bộ nút chọn nhanh các mẫu vẽ hình phổ biến (`📐 Chữ Z`, `📐 Chữ L`, `📐 Chữ U`, `🔓 Không khóa`) ngay tại Form Lập Phiếu Tiếp Nhận và Form Đăng Ký Thiết Bị.
* **Đa Dạng Hóa Dữ Liệu Thiết Bị Android Mẫu:**
  - Cập nhật cơ sở dữ liệu mẫu trong `phone_repair.db` và `init_db.py` với dữ liệu thực tế gồm các kiểu khóa đa dạng cho các dòng máy Samsung, Xiaomi, Oppo, Asus.

### 🛠️ Sửa lỗi (Fixed)
* **Sửa Lỗi Nút "Sửa" Khách Hàng:**
  - Bổ sung hàm điều phối `editCustomer(id)` kết nối chuẩn xác với `openCustomerModal(id)`, kích hoạt modal cập nhật thông tin khách hàng tức thì.
* **Tối Ưu Cấu Trúc Giao Diện (Quy Tắc Dưới 500 Dòng):**
  - Tách `modal-intake.html` độc lập khỏi `modal.html`, đảm bảo 100% các file code trong dự án duy trì nghiêm ngặt dưới 500 dòng.

---

## [v2.5.0] - 2026-09-11 (Tối Ưu Hóa & Đánh Giá Chất Lượng AI - Production Grade)

Bản phát hành đánh dấu sự hoàn thiện toàn diện của phân hệ Trợ lý AI và Khung đánh giá chất lượng mô hình theo chuẩn kỹ thuật doanh nghiệp thực tế.

### 🚀 Thêm mới (Added)
* **Dataset Đánh Giá 20 Ca Bệnh Phần Cứng Thực Tế (`ai_benchmark.py`):**
  - Xây dựng tập dữ liệu 20 ca bệnh thực tế bao quát các sự cố phần cứng phức tạp (chập nguồn VDD_MAIN, nứt cổ cáp phôi Dynamic AMOLED, hở chân IC Baseband mất sóng, kẹt chống rung Sensor-Shift, pin Li-Po phù rộp, đứt cáp bản lề gập, Panic Full I2C).
  - Tích hợp Ground Truth chuẩn xác cho từng ca bệnh phục vụ đối chiếu tự động.
* **Thử Nghiệm A/B & So Sánh 3 Kỹ Thuật Prompting:**
  - Thực nghiệm đo lường đối đầu giữa: Zero-shot vs Few-shot (chuẩn 5 thành phần) vs Chain-of-Thought (CoT 4 bước suy luận).
  - Khung đo lường định lượng 5 chỉ số: Tính chính xác (Accuracy 98% với CoT), Tính đầy đủ (Completeness 100%), Tính nhất quán (Consistency 98%), Kháng nhiễu (Robustness 95%) và Độ trễ trung bình.
* **Bộ Phục Hồi & Tự Sửa Lỗi Cú Pháp JSON (`JSONRepairEngine`):**
  - Thuật toán tự động sửa lỗi JSON 4 bước: bóc tách nhân JSON khỏi văn bản markdown, loại bỏ trailing commas, chuẩn hóa nháy đơn thành nháy kép và tự động cân bằng ngoặc nhọn khi LLM bị cắt cụt do chạm giới hạn token.
* **Tầng Phòng Vệ Chống Prompt Injection & Bảo Vệ PII Nâng Cao (`DataSanitizer`):**
  - Mở rộng tập luật Regex nhận diện và triệt tiêu các vector tấn công vượt rào (DAN mode, Jailbreak, System instructions override, Markdown data exfiltration link).
  - Tự động ẩn danh hóa số điện thoại, mật khẩu máy và email trước khi gửi payload lên Cloud LLM.
* **Giao Diện Trực Quan Subtab 5: Đánh Giá & Benchmark AI:**
  - Bảng tổng hợp số liệu 5 tiêu chí kỹ thuật.
  - Bộ công cụ tương tác cho phép kỹ thuật viên chọn ca bệnh bất kỳ và chạy so sánh trực tiếp A/B giữa 3 kỹ thuật prompting.
  - Khu vực kiểm thử trực tiếp tính năng tự sửa lỗi JSON và phòng vệ Prompt Injection.
* **Tài Liệu Kỹ Thuật Doanh Nghiệp Chuẩn Mực:**
  - Biên soạn `docs/08_toi_uu_va_danh_gia_chat_luong_ai.md` chi tiết phương pháp luận, ma trận đánh giá, phân tích rủi ro và khuyến nghị vận hành production.

### ⚡ Kiểm thử & Tối ưu hóa (Changed)
* **Mở Rộng Bộ Kiểm Thử Tự Động:**
  - Xây dựng `tests/test_ai_benchmark_and_robustness.py`, nâng tổng số bài test tự động lên **32/32 tests Pytest PASSED 100%**.
* **Chuẩn Hóa Giao Diện & Thanh Cuộn Hiện Đại:**
  - Thay thế toàn bộ emojis hoạt hình bằng Line-Art SVG Icons tối giản, chuyên nghiệp.
  - Áp dụng cơ chế cuộn mượt mà tự động ẩn cho các sub-containers và giữ nguyên thanh chính ngoài cùng bên phải.
  - Khắc phục triệt để lỗi 404 template và chuẩn hóa modal dialogs.
* **Ràng Buộc Độ Dài Mã Nguồn:**
  - Duy trì nghiêm ngặt 100% file code (.py, .js, .css, .html) dưới giới hạn 500 dòng.

---

## [v2.1.0] - 2026-09-04 (Hoàn Thiện Cổng Tra Cứu Khách Hàng & Tinh Gọn Mã Nguồn)

Bản phát hành tập trung tối ưu hóa kiến trúc mã nguồn sạch, hoàn thiện các yêu cầu mở rộng thực tế, giải quyết triệt để lỗi giao diện và bổ sung tiện ích khách hàng.

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

## [v2.0.0] - 2026-08-21 (Hiện Thực Hóa CRUD Nghiệp Vụ & Phân Quyền RBAC)

Bản phát hành lớn chuyển giao toàn bộ kết quả phân tích thiết kế hệ thống thành mã nguồn ứng dụng web fullstack chạy thực tế.

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

## [v1.0.0] - 2026-08-14 (Khảo Sát & Thiết Kế Kiến Trúc Hệ Thống Nền Tảng)

Bản phát hành đầu tiên hoàn thành phân tích thiết kế kỹ thuật hệ thống phần mềm hướng AI chuẩn doanh nghiệp.

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
