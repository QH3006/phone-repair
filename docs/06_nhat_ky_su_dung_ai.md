# 6. NHẬT KÝ SỬ DỤNG AI TRONG PHÂN TÍCH VÀ THIẾT KẾ (AI USAGE LOG - KT1)

Tuân thủ đúng quy định về thực hành môn học và tính minh bạch học thuật (AI-Augmented SDLC), bảng dưới đây ghi chép chi tiết toàn bộ các phiên làm việc cùng các công cụ AI trong giai đoạn Kiểm tra Thường xuyên 1 (Phân tích & Thiết kế hệ thống).

---

## 6.1. Bảng Tổng Hợp Nhật Ký Sử Dụng AI

| STT | Thời Gian | Nhiệm Vụ Kỹ Thuật | Công Cụ & Phiên Bản | Prompt Đã Sử Dụng (Input) | Phản Hồi Chính Của AI (Output) | Đánh Giá & Hiệu Chỉnh Của Sinh Viên (Human-in-the-loop) |
|---|---|---|---|---|---|---|
| **01** | 14/08/2026 09:30 | Khám phá yêu cầu nghiệp vụ & phân rã quy trình sửa chữa | ChatGPT (GPT-4o) | *"Bạn là chuyên viên phân tích nghiệp vụ. Hãy phân tích quy trình vận hành trung tâm sửa chữa điện thoại, chỉ ra các điểm nghẽn giao tiếp và đề xuất 8 trạng thái sửa chữa chuẩn."* | AI liệt kê 5 bước sửa chữa cơ bản và đề xuất các vai trò: Lễ tân, KTV, Quản lý. | **Chỉnh sửa**: Thấy rằng AI thiếu vai trò Thu ngân độc lập và thiếu trạng thái chờ khách duyệt báo giá (`BaoGia_ChoDuyet`). Sinh viên đã bổ sung thêm vai trò Thu ngân và hoàn thiện đủ 8 trạng thái vòng đời phiếu sửa. |
| **02** | 14/08/2026 11:15 | Thiết kế Cơ sở dữ liệu quan hệ (ERD & Data Dictionary) | Google Gemini 1.5 Pro | *"Đề xuất cấu trúc bảng CSDL SQLite cho hệ thống quản lý sửa chữa điện thoại có tích hợp AI, đảm bảo quan hệ 1:N, 1:1 và có bảng lưu vết log AI."* | AI đề xuất 6 bảng: `Users`, `Customers`, `Devices`, `RepairOrders`, `Parts`, `Invoices`. | **Chỉnh sửa**: AI chưa tách riêng bảng `DichVu` (tiền công) dẫn đến khó tính toán chi phí khi sửa chữa không thay linh kiện; thiếu bảng `BaoHanh` điện tử. Sinh viên đã thiết kế lại thành 10 bảng hoàn chỉnh với đầy đủ ràng buộc toàn vẹn. |
| **03** | 14/08/2026 14:00 | Thiết kế 3 bộ Prompt kỹ thuật 5 thành phần | Google Gemini 1.5 Pro | *"Thiết kế prompt tóm tắt lỗi kỹ thuật phần cứng điện thoại theo chuẩn 5 thành phần (Instructions, Context, Constraints, Examples, Output Format) trả về JSON."* | AI tạo khung prompt với instructions và output format mẫu, nhưng phần constraints còn sơ sài. | **Hiệu chỉnh**: Sinh viên bổ sung ràng buộc nghiêm ngặt về trường `risk_level` (`Thap`, `TrungBinh`, `Cao`), cấm mô hình tự suy diễn ngoài ghi chú (Anti-hallucination) và thêm ví dụ Few-shot sát thực tế phần cứng iPhone/Samsung. |
| **04** | 14/08/2026 15:45 | Phản biện bảo mật & thiết kế luồng phòng thủ ngoại lệ | Claude 3.5 Sonnet | *"Đóng vai trò chuyên gia an toàn thông tin, hãy phân tích các nguy cơ rò rỉ dữ liệu khi gửi thông tin sửa máy lên Cloud LLM và đề xuất phương án phòng thủ."* | AI cảnh báo nguy cơ lộ PII (SĐT, mật khẩu màn hình khách lưu trong CSDL) và tấn công Prompt Injection qua ô nhập mô tả lỗi. | **Áp dụng**: Sinh viên đã thiết kế module `Data Sanitization` tự động bóc tách PII trước khi gửi payload lên Gemini API và tích hợp cơ chế Fallback tĩnh khi timeout quá 5s. |

---

## 6.2. Đánh Giá Trải Nghiệm và Bài Học Rút Ra (Self-Reflection)
1. **AI là công cụ tăng cường (Augmentation Tool)**: AI giúp tăng tốc độ phác thảo sơ đồ và dàn ý tài liệu lên gấp 3 lần, tuy nhiên các chi tiết logic nghiệp vụ đặc thù (như bảo hành theo từng linh kiện, phân chia tiền công dịch vụ) bắt buộc phải do con người hiệu chỉnh.
2. **Tầm quan trọng của Prompt Engineering**: Thiết kế prompt có cấu trúc 5 thành phần giúp kết quả trả về ổn định, dự đoán được và dễ dàng parse tự động trong code hơn rất nhiều so với prompt tự do một câu.
3. **Bảo mật và Quyền riêng tư là ưu tiên hàng đầu**: Luôn ghi nhớ nguyên tắc không gửi dữ liệu nhạy cảm của người dùng lên các mô hình AI công cộng.
