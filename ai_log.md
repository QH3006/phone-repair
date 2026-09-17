# 📋 NHẬT KÝ SỬ DỤNG AI (AI USAGE & AUDIT LOG) — `ai_log.md`

> **Đề tài:** Hệ thống Quản lý Dịch vụ Sửa chữa Thiết bị Di động Tích hợp Trợ lý AI (PhoneCare AI)  
> **Các giai đoạn:** KT1 (Phân tích & Thiết kế) — KT2 (CRUD Nghiệp vụ & Phân quyền RBAC) — Định hướng KT3 (Tối ưu hóa & Đánh giá chất lượng)  
> **Quy trình áp dụng:** Phát triển phần mềm hiện đại có AI đồng hành (AI-Augmented SDLC) kết hợp Giám sát của Con người (**Human-in-the-Loop - HITL**)  

---

## 🎯 1. NGUYÊN TẮC SỬ DỤNG AI & GIỚI HẠN PHẠM VI (SCOPE BOUNDARY)

### 1.1. Nguyên tắc đạo đức & An toàn kỹ thuật
1. **Human-in-the-loop (Con người quyết định tối thượng):** Mọi mã nguồn, thiết kế CSDL, quy trình nghiệp vụ và prompt do AI đề xuất đều phải qua bước phản biện, kiểm thử và hiệu chỉnh của sinh viên/kỹ sư trước khi đưa vào hệ thống. Tuyệt đối không sao chép nguyên văn khi chưa hiểu rõ bản chất.
2. **Bảo mật dữ liệu riêng tư (PII Protection):** Không gửi dữ liệu định danh khách hàng (SĐT thật, IMEI, mật khẩu máy) lên các mô hình AI đám mây công cộng. Dự án xây dựng module `DataSanitizer` để che mờ dữ liệu trước khi gọi AI.
3. **Phòng vệ chống ảo giác (Anti-Hallucination):** Ép buộc mô hình trả về cấu trúc Strict JSON Schema thông qua Pydantic Validation; xây dựng Fallback Engine khi API lỗi/timeout.

### 1.2. Làm rõ phạm vi đồ án (Khắc phục hiện tượng "Tham phạm vi")
Để khắc phục nhược điểm "tài liệu hơi tham phạm vi", đồ án phân định ranh giới kỹ thuật rõ ràng:
- **Phạm vi CỐT LÕI bắt buộc (In-Scope - Trọng tâm KT1 & KT2):**
  - Quản lý quy trình sửa chữa qua 8 trạng thái kỹ thuật chuẩn.
  - Hoàn thiện 100% CRUD 5 phân hệ: Khách hàng & Thiết bị, Kho linh kiện & Dịch vụ, Phiếu sửa chữa & Chi tiết thay thế, Hóa đơn & Sổ bảo hành điện tử, Quản trị nhân sự.
  - Xác thực bảo mật JWT Bearer Token + Phân quyền RBAC 4 vai trò rõ ràng (`QuanLy`, `LeTan`, `KyThuatVien`, `ThuNgan`).
  - 3 Chức năng Trợ lý AI phục vụ trực tiếp nghiệp vụ: (1) Tóm tắt lỗi kỹ thuật từ ghi chú KTV, (2) Giải thích linh kiện/dịch vụ bằng ngôn ngữ bình dân, (3) Tự động soạn thảo SMS/Zalo cập nhật tiến độ cho khách.
  - Bộ kiểm thử tự động `pytest` kiểm chứng toàn bộ luồng Auth, RBAC, CRUD và AI.
- **Phần nghiên cứu mở rộng (Experimental / Out-of-Scope - Tùy chọn):**
  - Các module thử nghiệm như RAG tra cứu cẩm nang sửa chữa, AI Sandbox thử nghiệm đa mô hình là các tính năng nghiên cứu chuyên sâu bổ sung, được tách biệt thành module độc lập, **không làm ảnh hưởng hay làm loãng luồng nghiệp vụ CRUD cốt lõi**.

---

## 📊 2. BẢNG NHẬT KÝ SỬ DỤNG AI CHI TIẾT THEO CÁC GIAI ĐOẠN

| STT | Giai đoạn | Thời gian | Nhiệm vụ kỹ thuật | Công cụ & Model | Prompt đã sử dụng (Input) | Phản hồi chính của AI (Output) | Đánh giá & Hiệu chỉnh của Kỹ sư (Human-in-the-Loop) | Kết quả áp dụng trong mã nguồn |
|:---:|:---:|:---:|:---|:---|:---|:---|:---|:---|
| **01** | **KT1** | 14/08/2026 09:30 | Phân tích bài toán & Khảo sát nghiệp vụ sửa chữa | ChatGPT (GPT-4o) | *"Bạn là chuyên viên phân tích nghiệp vụ. Hãy phân tích quy trình vận hành trung tâm sửa chữa điện thoại, chỉ ra các điểm nghẽn giao tiếp và đề xuất các trạng thái sửa chữa chuẩn."* | AI liệt kê 5 bước sửa chữa cơ bản và đề xuất gộp chung Lễ tân với Thu ngân. | **BÁC BỎ & BỔ SUNG:** Bác bỏ việc gộp vai trò vì trung tâm cần tách bạch tài chính. Bổ sung trạng thái chờ khách duyệt báo giá (`BaoGia_ChoDuyet`) để hoàn thiện đủ 8 trạng thái chuẩn. | [`docs/01_bai_toan_va_yeu_cau.md`](docs/01_bai_toan_va_yeu_cau.md) |
| **02** | **KT1** | 14/08/2026 11:15 | Thiết kế Cơ sở dữ liệu quan hệ (ERD & Schema) | Google Gemini 1.5 Pro | *"Đề xuất cấu trúc bảng CSDL SQLite cho hệ thống quản lý sửa chữa điện thoại có tích hợp AI, đảm bảo quan hệ 1:N, 1:1 và có bảng lưu vết log AI."* | AI đề xuất 6 bảng: `Users`, `Customers`, `Devices`, `RepairOrders`, `Parts`, `Invoices`. | **CHỈNH SỬA:** AI gộp chung tiền linh kiện và tiền công dịch vụ vào một chỗ, thiếu bảng `BaoHanh` điện tử. Kỹ sư tách riêng bảng `dich_vu` và `linh_kien`, bổ sung bảng `bao_hanh` và `ai_logs`. | [`backend/app/db/models.py`](backend/app/db/models.py) |
| **03** | **KT1** | 14/08/2026 14:00 | Thiết kế Prompt 5 thành phần & Guardrails an toàn | Google Gemini 1.5 Pro | *"Thiết kế prompt tóm tắt lỗi kỹ thuật phần cứng điện thoại theo chuẩn 5 thành phần (Instructions, Context, Constraints, Examples, Output Format) trả về JSON."* | AI sinh khung prompt với instructions nhưng phần constraints còn lỏng lẻo, trả lời tự do bằng Markdown. | **HIỆU CHỈNH NGHIÊM NGẶT:** Bắt buộc cấu trúc Strict JSON Schema bằng Pydantic; cấm mô hình suy diễn ngoài ghi chú (Anti-hallucination); bổ sung 3 ví dụ Few-shot thực tế. | [`docs/05_thiet_ke_prompt_va_luong_ai.md`](docs/05_thiet_ke_prompt_va_luong_ai.md) |
| **04** | **KT1** | 14/08/2026 15:45 | Phản biện bảo mật & Phòng thủ dữ liệu | Claude 3.5 Sonnet | *"Đóng vai trò chuyên gia an toàn thông tin, hãy phân tích nguy cơ rò rỉ dữ liệu khi gửi thông tin sửa máy lên Cloud LLM và đề xuất phương án phòng thủ."* | AI cảnh báo nguy cơ lộ PII (SĐT khách, mật khẩu màn hình) và tấn công Prompt Injection. | **ÁP DỤNG:** Lập trình module `DataSanitizer` tự động bóc tách PII trước khi gửi payload lên Gemini API và tích hợp cơ chế Fallback tĩnh khi timeout quá 5s. | [`backend/app/services/ai_service.py`](backend/app/services/ai_service.py) |
| **05** | **KT2** | 20/08/2026 08:30 | Xây dựng Data Models (SQLAlchemy ORM) & Schemas (Pydantic V2) | Google Gemini 1.5 Flash | *"Viết mã nguồn SQLAlchemy ORM models và Pydantic V2 schemas cho 8 thực thể của hệ thống sửa chữa điện thoại, có relationships và cascaded delete hợp lý."* | AI sinh code SQLAlchemy 1.4 cũ dùng cú pháp `declarative_base()` và Pydantic V1 (`class Config: orm_mode = True`). | **TÁI CẤU TRÚC:** Kỹ sư nâng cấp toàn bộ lên cú pháp Pydantic V2 chuẩn (`model_config = ConfigDict(from_attributes=True)`), thêm các trường validator kiểm tra định dạng SĐT (10 số) và giá tiền $\ge 0$. | [`backend/app/schemas/schemas.py`](backend/app/schemas/schemas.py) |
| **06** | **KT2** | 20/08/2026 14:00 | Triển khai Xác thực JWT & Phân quyền RBAC Guard | ChatGPT (GPT-4o) | *"Tạo FastAPI security dependencies kiểm tra quyền truy cập dựa trên JWT token, hỗ trợ 4 vai trò QuanLy, LeTan, KyThuatVien, ThuNgan với mã lỗi 401 và 403."* | AI viết hàm kiểm tra quyền nhưng hardcode danh sách vai trò dạng chuỗi rời rạc ở từng endpoint, gây trùng lặp mã nguồn. | **TỐI ƯU HÓA:** Thiết kế hàm decorator / dependency factory `require_roles(*allowed_roles)` tái sử dụng linh hoạt; chuẩn hóa mã lỗi HTTP 401 (chưa đăng nhập) và 403 (không đủ quyền). | [`backend/app/core/security.py`](backend/app/core/security.py) |
| **07** | **KT2** | 21/08/2026 09:15 | Hiện thực hóa CRUD Phiếu Sửa Chữa & Tính toán tự động | Google Gemini 1.5 Flash | *"Viết router FastAPI cho CRUD Phiếu Sửa Chữa (`/api/repairs`). Khi kỹ thuật viên thêm linh kiện hoặc dịch vụ vào phiếu, tự động cập nhật lại tổng tiền phiếu sửa."* | AI tạo router nhưng không dùng database transaction (`db.commit()`), dễ gây sai lệch số liệu nếu một linh kiện thêm bị lỗi. | **HOÀN THIỆN:** Đưa toàn bộ nghiệp vụ cập nhật linh kiện, dịch vụ và tính lại tổng tiền vào Transaction an toàn; đồng thời cập nhật tự động trừ tồn kho linh kiện (`so_luong_ton`). | [`backend/app/api/routers/repairs.py`](backend/app/api/routers/repairs.py) |
| **08** | **KT2** | 21/08/2026 16:30 | Tự động hóa Cấp Thẻ Bảo Hành Điện Tử & Lập Hóa Đơn | Claude 3.5 Sonnet | *"Tư vấn logic nghiệp vụ: Khi Thu ngân lập hóa đơn thanh toán thành công, hệ thống cần tự động kích hoạt những gì?"* | AI đề xuất: cập nhật trạng thái phiếu sửa sang `DaThanhToan` và tự động sinh bản ghi bảo hành điện tử cho từng linh kiện có thời hạn bảo hành $> 0$. | **ÁP DỤNG:** Hiện thực hóa API `/api/invoices`: Khi thanh toán thành công, tự động cấp mã bảo hành dạng `BH-YYYYMMDD-XXX` với hạn dùng theo đúng số tháng bảo hành của linh kiện. | [`backend/app/api/routers/invoices.py`](backend/app/api/routers/invoices.py) |
| **09** | **KT2** | 22/08/2026 10:00 | Xây dựng Bộ Kiểm Thử Tự Động Toàn Diện (`pytest`) | ChatGPT (GPT-4o) | *"Viết bộ test suite tự động bằng pytest kiểm tra toàn bộ luồng đăng nhập, phân quyền RBAC và CRUD của các endpoint chính."* | AI sinh 15 test cases đơn giản nhưng thiếu test trường hợp từ chối quyền (403 Forbidden) và thiếu test phân hệ AI Fallback. | **MỞ RỘNG:** Kỹ sư mở rộng thành bộ test toàn diện 35 test cases (chia thành các test file chuyên biệt: Auth, CRUD, RBAC, AI Prompt, Browser live static), đảm bảo độ bao phủ 100% các luồng cốt lõi. | [`tests/`](tests/) |
| **10** | **KT2** | 22/08/2026 15:00 | Tái cấu trúc Giao diện Web Modular & Form Validation | Google Gemini 1.5 Flash | *"Tư vấn cách phân chia file JavaScript và CSS cho ứng dụng SPA Vanilla để tránh bị phình to (monolithic file)."* | AI đề xuất chia JavaScript thành các modules theo tính năng nghiệp vụ (`auth.js`, `repairs.js`, `customers.js`, `billing.js`,...) và CSS theo tầng layout/components. | **ÁP DỤNG:** Tách thành 14 modules JS độc lập, nạp qua `index.html` với cơ chế cache buster versioning (`?v=62`), giúp code sáng sủa, dễ bảo trì và không bị xung đột. | [`frontend/js/modules/`](frontend/js/modules/) |

---

## 💡 3. TỔNG KẾT BÀI HỌC VÀ ĐÁNH GIÁ NĂNG SUẤT (SELF-REFLECTION)

### 3.1. Đánh giá định lượng hiệu quả (Productivity Impact)
- **Tốc độ phác thảo ban đầu (Prototyping Speed):** Sử dụng AI giúp rút ngắn thời gian viết boilerplate code (SQLAlchemy models, Pydantic schemas, khung router FastAPI) khoảng **60% - 70%** so với viết thủ công từ đầu.
- **Tốc độ sinh dữ liệu kiểm thử (Test Data Generation):** AI hỗ trợ tạo ra 20 ca bệnh mẫu sát thực tế phần cứng (iPhone chai pin, Samsung hỏng cáp màn hình, Xiaomi mất nguồn,...) phục vụ kiểm thử prompt và test CSDL chỉ trong vài phút.

### 3.2. Những hạn chế của AI được phát hiện và bài học thực tiễn
1. **AI thường sinh mã lỗi thời hoặc thiếu an toàn:**
   - Khi không chỉ định phiên bản, AI thường sinh mã Pydantic V1 cũ (`class Config`) hoặc SQLAlchemy 1.4, đòi hỏi kỹ sư phải nắm vững kiến trúc phiên bản mới để prompt chính xác hoặc hiệu chỉnh lại.
   - AI có xu hướng bỏ qua database transaction và xử lý lỗi biên (edge cases như chia cho 0, chuỗi rỗng, số âm).
2. **AI không thể thay thế con người trong quyết định nghiệp vụ:**
   - Việc phân chia vai trò trung tâm (tách Lễ tân và Thu ngân, phân quyền KTV chỉ được thao tác phiếu của mình) bắt nguồn từ thực tế quản trị vận hành, AI không tự hiểu được nếu không có chuyên gia con người định hướng.
3. **Cảnh giác với "Tham phạm vi" (Scope Creep):**
   - AI rất hay đề xuất các công nghệ hào nhoáng (RAG vector, microservices, đa đám mây) vượt quá yêu cầu môn học. Sinh viên/kỹ sư cần tỉnh táo giữ vững ranh giới phạm vi: tập trung làm xuất sắc, hoàn thiện và tin cậy các tính năng nghiệp vụ cốt lõi trước tiên.

---

## 🔗 4. LIÊN KẾT TÀI LIỆU MINH CHỨNG LIÊN QUAN
- **Báo cáo Phân tích & Thiết kế (KT1):** [`BAO_CAO_KT1_PHAN_TICH_THIET_KE.md`](BAO_CAO_KT1_PHAN_TICH_THIET_KE.md)
- **Báo cáo CRUD & Phân quyền RBAC (KT2):** [`BAO_CAO_KT2_TRIEN_KHAI_CRUD_RBAC.md`](BAO_CAO_KT2_TRIEN_KHAI_CRUD_RBAC.md)
- **Minh chứng chi tiết từng phiên tương tác:** [`docs/ai-evidence/KT1/`](docs/ai-evidence/KT1/)
- **Bảng tóm tắt nội bộ:** [`docs/06_nhat_ky_su_dung_ai.md`](docs/06_nhat_ky_su_dung_ai.md)
- **Bộ kiểm thử tự động xác thực hệ thống:** [`tests/`](tests/)
