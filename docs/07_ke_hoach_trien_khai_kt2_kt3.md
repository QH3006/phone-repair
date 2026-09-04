# 7. KẾ HOẠCH TRIỂN KHAI CHO CÁC GIAI ĐOẠN TIẾP THEO (KT2, KT3, CUỐI KỲ)

Để đảm bảo dự án phát triển liên tục, đúng tiến độ và kế thừa trọn vẹn kết quả phân tích thiết kế của Kiểm tra Thường xuyên 1 (KT1), dưới đây là lộ trình triển khai chi tiết cho các giai đoạn tiếp theo.

---

## 7.1. Giai đoạn Kiểm tra Thường xuyên 2 (KT2): Xây dựng CRUD Nghiệp Vụ & Phân Quyền

### Mục tiêu cốt lõi:
Xây dựng hoàn chỉnh hệ thống quản trị cốt lõi, cơ chế xác thực phân quyền và các luồng nghiệp vụ cơ bản.

### Danh mục công việc chi tiết:
1. **Hoàn thiện Cấu trúc mã nguồn Backend & Frontend**:
   - Cấu trúc module hóa: `routers/`, `schemas/`, `crud/`, `services/`, `core/`.
2. **Cơ chế Xác thực và Phân quyền (Auth & RBAC)**:
   - Đăng nhập JWT, băm mật khẩu `bcrypt`.
   - Phân quyền 4 vai trò: `QuanLy`, `LeTan`, `KyThuatVien`, `ThuNgan`.
   - Middleware kiểm tra quyền truy cập trên từng API endpoint.
3. **Hoàn thiện CRUD các thực thể chính**:
   - Quản lý Khách hàng (`/api/customers`) và Thiết bị (`/api/devices`).
   - Quản lý Kho Linh kiện (`/api/parts`) và Danh mục Dịch vụ (`/api/services`).
   - Quản lý Phiếu sửa chữa (`/api/repairs`): Tiếp nhận, phân công KTV, cập nhật trạng thái vòng đời.
4. **Tính năng Tìm kiếm, Lọc & Phân trang**:
   - Tìm kiếm nhanh phiếu sửa theo Số điện thoại, Mã phiếu, IMEI.
   - Lọc danh sách theo Trạng thái sửa chữa, KTV phụ trách, Khoảng thời gian.
5. **Dashboard Thống kê cơ bản**:
   - Thống kê tổng số phiếu tiếp nhận trong ngày/tuần.
   - Doanh thu ước tính và biểu đồ tỷ lệ các loại bệnh máy phổ biến.
6. **Xử lý ngoại lệ & Tính ổn định**:
   - Validation dữ liệu đầu vào với Pydantic.
   - Bắt lỗi CSDL, mã lỗi HTTP chuẩn (400, 401, 403, 404, 422, 500).

---

## 7.2. Giai đoạn Kiểm tra Thường xuyên 3 (KT3): Tối ưu hóa & Kiểm thử Chức năng AI

### Mục tiêu cốt lõi:
Tích hợp sâu, tối ưu hóa toàn diện 3 chức năng AI, thiết kế bộ kiểm thử tự động và review chất lượng code bằng AI.

### Danh mục công việc chi tiết:
1. **Tích hợp sâu Google Gemini API**:
   - Kết nối API chính thức, quản lý API key bảo mật qua `.env`.
   - Xử lý dữ liệu động trực tiếp từ CSDL SQLite.
2. **Tối ưu Prompt qua 3 vòng thử nghiệm (Prompt Optimization Cycle)**:
   - Thử nghiệm so sánh kỹ thuật: Zero-shot vs Few-shot vs Chain-of-Thought (CoT).
   - Đánh giá chất lượng đầu ra trên 20 ca bệnh thực tế theo 5 tiêu chí: Tính chính xác (Accuracy), Tính đầy đủ (Completeness), Tính nhất quán (Consistency), Tính mạnh mẽ (Robustness) và Tốc độ (Performance).
3. **Hoàn thiện Bộ Xử Lý Ngoại Lệ & Phòng Thủ AI**:
   - Triển khai bộ Regex JSON Repair khi model sinh định dạng lỗi.
   - Fallback tĩnh tự động khi API Timeout ($>5\text{s}$).
   - Kiểm thử phòng thủ Prompt Injection và rò rỉ dữ liệu (Prompt Leaking).
4. **Kiểm thử Tự động Toàn Diện (Automated Testing with Pytest)**:
   - Viết unit test cho các hàm xử lý dữ liệu và CRUD.
   - Viết integration test cho API endpoints và luồng gọi AI.
   - Kiểm thử các trường hợp dữ liệu thiếu, dữ liệu rác và trường hợp biên (edge cases).
5. **Review Mã Nguồn & Tối ưu bằng AI**:
   - Sử dụng AI để rà soát lỗ hổng bảo mật, phát hiện code smells và refactor mã nguồn.

---

## 7.3. Giai đoạn Thi Kết Thúc Học Phần (Final Capstone)

### Mục tiêu cốt lõi:
Đóng gói sản phẩm hoàn chỉnh, viết báo cáo kỹ thuật tổng hợp toàn diện và thực hiện thuyết trình demo trực quan.

### Danh mục công việc chi tiết:
1. **Hoàn thiện & Tinh chỉnh Toàn Bộ Hệ Thống**:
   - Kiểm tra vận hành ổn định trên môi trường sạch (Clean Environment).
   - Tạo bộ Seed Data phong phú phục vụ demo thuyết trình (đầy đủ các kịch bản thực tế).
2. **Đóng gói & Hướng dẫn Cài đặt**:
   - File `README.md` hướng dẫn chạy trong 3 bước.
   - File cấu hình môi trường `.env.example` và `requirements.txt`.
3. **Báo cáo Kỹ thuật Tổng Hợp**:
   - Tổng kết toàn bộ quá trình áp dụng AI trong SDLC (Phân tích $\rightarrow$ Thiết kế $\rightarrow$ Lập trình $\rightarrow$ Kiểm thử $\rightarrow$ Vận hành).
   - Đánh giá định lượng hiệu quả sử dụng AI theo các framework DORA, SPACE và DevX.
4. **Kịch bản Demo & Slide Thuyết Trình**:
   - Kịch bản demo mạch lạc: Tiếp nhận $\rightarrow$ KTV khám máy & dùng AI $\rightarrow$ Khách xem giải thích & nhận SMS $\rightarrow$ Thu ngân lập hóa đơn & bảo hành.
