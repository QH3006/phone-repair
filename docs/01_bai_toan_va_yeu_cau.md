# 1. MÔ TẢ BÀI TOÁN VÀ YÊU CẦU HỆ THỐNG

## 1.1. Bối cảnh hoạt động
Trung tâm bảo dưỡng và sửa chữa thiết bị di động thông minh PhoneCare là đơn vị chuyên cung cấp dịch vụ tiếp nhận, chẩn đoán, thay thế linh kiện chính hãng và bảo hành thiết bị di động (smartphone, tablet). Hệ thống vận hành cần kết nối chặt chẽ giữa các bộ phận: Lễ tân tiếp đón, Kỹ thuật viên (KTV) sửa chữa, Thu ngân thanh toán và Ban Quản lý trung tâm.

## 1.2. Các tác nhân và vai trò trong hệ thống
- **Quản lý (Manager/Admin)**: Quản trị tài khoản nhân sự, phân quyền vai trò (RBAC), quản lý danh mục giá linh kiện/dịch vụ, xem báo cáo doanh thu và đánh giá năng suất KTV.
- **Lễ tân (Receptionist)**: Tiếp nhận thiết bị, lập phiếu sửa chữa ban đầu, phân công hoặc điều phối KTV, tra cứu tiến độ, kích hoạt AI sinh tin nhắn gửi khách hàng (SMS/Zalo) và bàn giao thiết bị.
- **Kỹ thuật viên (Technician)**: Tiếp nhận máy được phân công, thực hiện đo đạc và chẩn đoán phần cứng, nhập ghi chú kỹ thuật, sử dụng trợ lý AI tóm tắt lỗi chuẩn hóa, đề xuất linh kiện thay thế và cập nhật trạng thái sửa chữa.
- **Thu ngân (Cashier)**: Lập hóa đơn thanh toán dịch vụ và linh kiện, thu tiền, in biên lai thanh toán và kích hoạt phiếu bảo hành điện tử.
- **Khách hàng (Customer)**: Tra cứu trực tuyến tiến độ sửa máy qua mã phiếu hoặc mã QR, đọc phần giải thích lỗi do AI tạo bằng ngôn ngữ đời thường.

## 1.3. Yêu cầu chức năng chi tiết (Functional Requirements - FRs)

### FR-01: Đăng nhập & Phân quyền
- **Input**: Tên đăng nhập, mật khẩu.
- **Processing**: Xác thực thông tin qua CSDL, kiểm tra mật khẩu băm bcrypt, sinh mã JWT token kèm danh sách quyền/vai trò.
- **Output**: Token phiên làm việc và giao diện điều hướng tương ứng với vai trò.

### FR-02: Quản lý Khách hàng & Thiết bị
- **Input**: Họ tên khách, Số điện thoại, Địa chỉ, Hãng sản xuất, Model máy, Số IMEI/Serial, Mật khẩu máy (nếu có).
- **Processing**: Kiểm tra trùng lặp SĐT/IMEI, tạo bản ghi khách hàng và thiết bị trong CSDL.
- **Output**: Hồ sơ khách hàng và thiết bị định danh thành công.

### FR-03: Tiếp nhận máy & Lập phiếu sửa chữa
- **Input**: ID Khách hàng, ID Thiết bị, Mô tả lỗi ban đầu từ khách hàng, Tình trạng ngoại quan, Phụ kiện kèm theo.
- **Processing**: Tạo bản ghi Phiếu sửa chữa mới với mã tự sinh (`PSC-YYYYMMDD-XXXX`), gán trạng thái `TiepNhan`.
- **Output**: Phiếu tiếp nhận được tạo thành công, in biên nhận có mã QR tra cứu.

### FR-04: Phân công Kỹ thuật viên
- **Input**: Mã phiếu sửa chữa, ID Kỹ thuật viên phụ trách.
- **Processing**: Gán KTV vào phiếu, chuyển trạng thái phiếu sang `PhanCongKTV`.
- **Output**: Thông báo việc mới gửi đến KTV, cập nhật trạng thái trên bảng điều khiển.

### FR-05: Chẩn đoán & Cập nhật trạng thái sửa chữa
- **Input**: Mã phiếu, Ghi chú kiểm tra kỹ thuật của KTV, Trạng thái chuyển đổi (`DangKiemTra`, `DangSuaChua`, `DaSuaXong`,...).
- **Processing**: Ghi nhận chi tiết kỹ thuật phần cứng, cập nhật tiến độ vào CSDL và lưu vết thời gian thay đổi.
- **Output**: Trạng thái phiếu được cập nhật thời gian thực.

### FR-06: Quản lý Linh kiện & Dịch vụ
- **Input**: Tên linh kiện/dịch vụ, Mã linh kiện, Đơn giá nhập, Đơn giá bán, Số lượng nhập/xuất kho.
- **Processing**: Quản lý tồn kho linh kiện; tự động trừ tồn kho khi linh kiện được đưa vào phiếu sửa chữa.
- **Output**: Báo cáo tồn kho linh kiện, cảnh báo linh kiện dưới định mức an toàn.

### FR-07: Thanh toán & Lập hóa đơn
- **Input**: Mã phiếu sửa chữa, Phương thức thanh toán (Tiền mặt, Chuyển khoản VietQR).
- **Processing**: Tổng hợp chi phí công thợ + linh kiện thay thế, lập bản ghi hóa đơn, cập nhật trạng thái phiếu `DaThanhToan`.
- **Output**: Hóa đơn thanh toán hoàn chỉnh có mã tra cứu.

### FR-08: Quản lý Bảo hành sau sửa chữa
- **Input**: Mã phiếu sửa chữa đã thanh toán, Thời hạn bảo hành của từng linh kiện.
- **Processing**: Tự động sinh mã bảo hành điện tử, tính ngày hết hạn bảo hành cho từng hạng mục sửa chữa.
- **Output**: Thẻ bảo hành điện tử và cập nhật trạng thái `HoanTat_TraMay`.

### FR-09: Báo cáo & Thống kê doanh thu
- **Input**: Khoảng thời gian thống kê (Từ ngày - Đến ngày), Tiêu chí lọc.
- **Processing**: Truy vấn tổng hợp doanh thu, đếm tần suất lỗi phần cứng phổ biến, thống kê linh kiện tiêu hao và hiệu suất KTV.
- **Output**: Biểu đồ trực quan và bảng số liệu thống kê chi tiết.

### FR-10: AI Tóm tắt tình trạng máy (Phân hệ KTV)
- **Input**: Ghi chú kỹ thuật thô của KTV, Model máy, Mô tả lỗi ban đầu của khách.
- **Processing**: Tiền xử lý làm sạch PII $\rightarrow$ Đóng gói Prompt 5 thành phần $\rightarrow$ Gọi Gemini API $\rightarrow$ Validate JSON schema $\rightarrow$ Ghi log `NhatKyAI`.
- **Output**: Bản tóm tắt chuẩn hóa: Hiện tượng phần cứng, Linh kiện hỏng, Đề xuất xử lý, Mức độ rủi ro (`Thap`, `TrungBinh`, `Cao`).

### FR-11: AI Sinh tin nhắn tiến độ (Phân hệ Lễ tân/CSKH)
- **Input**: Tên khách, Model máy, Trạng thái sửa chữa, Tổng chi phí dự kiến, Ngày giờ hẹn trả.
- **Processing**: Đóng gói Prompt theo kênh gửi (SMS dưới 160 ký tự, Zalo dưới 250 từ), gọi Gemini API tạo lời nhắn lịch sự, minh bạch.
- **Output**: Đoạn văn bản tin nhắn sẵn sàng gửi qua SMS/Zalo Gateway.

### FR-12: AI Diễn giải lỗi & Dịch vụ (Phân hệ Khách hàng tra cứu)
- **Input**: Tên linh kiện cần thay, Tên gói dịch vụ, Bản tóm tắt lỗi kỹ thuật đã duyệt.
- **Processing**: Đóng gói Prompt tư vấn sử dụng hình ảnh so sánh đời thường (metaphor), gọi Gemini API giải thích lý do cần thay thế.
- **Output**: Đoạn giải thích ngắn gọn, dễ hiểu, xóa bỏ rào cản thuật ngữ chuyên môn.

## 1.4. Yêu cầu phi chức năng (Non-Functional Requirements - NFRs)
1. **Bảo mật & Phân quyền**:
   - Xác thực JWT token, băm mật khẩu bcrypt.
   - Cơ chế Phân quyền dựa trên vai trò (RBAC) nghiêm ngặt tại Backend.
   - Bảo mật thông tin định danh cá nhân (PII Data Sanitization) trước khi chuyển dữ liệu qua AI API.
2. **Hiệu năng**:
   - Thời gian đáp ứng các API CRUD nghiệp vụ $< 200\text{ms}$.
   - Thời gian xử lý AI trung bình $1.5\text{s} - 3.0\text{s}$, cấu hình Timeout tối đa $5.0\text{s}$ kèm cơ chế Fallback tĩnh.
3. **Độ tin cậy & Tính sẵn sàng**:
   - Ứng dụng không bao giờ bị crash khi LLM API gặp sự cố hoặc trả về phản hồi sai cấu trúc.
   - CSDL SQLite có cơ chế sao lưu tự động định kỳ.
4. **Khả năng sử dụng (Usability)**:
   - Giao diện đáp ứng (Responsive), hiện đại, tối ưu cho cả máy tính Lễ tân/Quản lý và thiết bị di động của KTV.
