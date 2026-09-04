# 🤖 MINH CHỨNG SỬ DỤNG AI TRONG PHÂN TÍCH YÊU CẦU & THIẾT KẾ USE CASE (KT1)
> **Nhiệm vụ**: Khảo sát bài toán quản lý sửa chữa điện thoại, phân rã quy trình 8 bước và thiết kế Use Case Diagram.

---

### 1. PROMPT GỬI AI (ChatGPT / Google Gemini 1.5 Pro)
```text
Bạn là chuyên gia Phân tích Thiết kế Hệ thống (Business Analyst / System Architect).
Hãy giúp tôi phân tích quy trình nghiệp vụ cho "Hệ thống Quản lý Trung tâm Sửa chữa Điện thoại di động có tích hợp AI".
Quy mô trung tâm: 8-12 nhân sự, 30-80 máy/ngày.

Yêu cầu:
1. Liệt kê các tác nhân (Actors) và công việc hàng ngày của họ.
2. Phân tích luồng quy trình sửa chữa từ lúc tiếp nhận đến khi bàn giao máy.
3. Xác định các điểm nghẽn nghiệp vụ (Pain points) có thể ứng dụng AI để tối ưu hóa.
4. Đề xuất danh sách Ca sử dụng (Use Cases) chính và vẽ sơ đồ Use Case dạng văn bản/Mermaid.
```

---

### 2. PHẢN HỒI GỐC CỦA AI (Tóm tắt Output)
* **AI đề xuất các tác nhân**:
  - *Admin*: Quản lý toàn bộ hệ thống.
  - *Nhân viên*: Làm cả việc tiếp nhận khách, báo giá và thu tiền.
  - *Kỹ thuật viên*: Kiểm tra và sửa chữa máy.
  - *Khách hàng*: Tra cứu đơn hàng.
* **AI đề xuất quy trình 6 bước**:
  - `Tiếp nhận` -> `Kiểm tra` -> `Báo giá` -> `Sửa chữa` -> `Thanh toán` -> `Trả máy`.
* **AI đề xuất chức năng AI**:
  - AI tự động chẩn đoán lỗi và tự động đặt mua linh kiện từ nhà cung cấp.

---

### 3. ĐÁNH GIÁ, PHẢN BIỆN VÀ HIỆU CHỈNH CỦA KỸ SƯ (Human Review & Refine)

| Thành phần | AI đề xuất ban đầu | Đánh giá của Kỹ sư | Quyết định điều chỉnh / Bác bỏ |
|---|---|---|---|
| **Phân định vai trò tác nhân** | Gộp chung "Nhân viên" làm cả Lễ tân và Thu ngân. | Chưa sát thực tế trung tâm chuyên nghiệp; có rủi ro thất thoát tài chính nếu lễ tân tự thu tiền và tự sửa giá. | **SỬA ĐỔI**: Tách thành 4 vai trò RBAC độc lập: `QuanLy`, `LeTan`, `KyThuatVien`, `ThuNgan` (chỉ Thu ngân mới được lập hóa đơn và xác nhận thanh toán). |
| **Vòng đời trạng thái phiếu** | 6 trạng thái cơ bản. | Thiếu bước phân công KTV và bước kiểm tra chất lượng (QC) sau sửa. | **BỔ SUNG**: Chuẩn hóa thành 8 trạng thái kỹ thuật: `TiepNhan` $\rightarrow$ `PhanCongKTV` $\rightarrow$ `DangKiemTra` $\rightarrow$ `BaoGia_ChoDuyet` $\rightarrow$ `DangSuaChua` $\rightarrow$ `DaSuaXong` $\rightarrow$ `DaThanhToan` $\rightarrow$ `HoanTat_TraMay`. |
| **Phạm vi tự động hóa của AI** | AI tự động quyết định giá và tự động đặt linh kiện. | Quá rủi ro (AI Hallucination), vi phạm nguyên tắc an toàn phần mềm y tế/kỹ thuật. | **BÁC BỎ & CHỈNH SỬA**: Giới hạn AI chỉ đóng vai trò trợ lý gợi ý (Advisor), áp dụng cơ chế **Human-in-the-Loop (HITL)**: Mọi đề xuất của AI đều phải qua KTV/Lễ tân xem xét và bấm nút duyệt trước khi ghi CSDL. |
