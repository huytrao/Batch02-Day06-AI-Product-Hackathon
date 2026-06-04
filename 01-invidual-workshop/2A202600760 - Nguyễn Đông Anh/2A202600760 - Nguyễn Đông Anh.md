# BÁO CÁO ĐÁNH GIÁ THỬ NGHIỆM CHATBOT MONI (MOMO)

- **Người thực hiện:** Nguyễn Đông Anh
- **Ngày kiểm thử:** 03/06/2026
- **Mục tiêu:** Đánh giá năng lực xử lý ngôn ngữ, độ chính xác của dữ liệu tài chính/tiện ích và trải nghiệm người dùng (UX) của Chatbot Moni trên hệ sinh thái MoMo.

---

## 1. Tổng Quan Về Chatbot Moni
Moni là trợ lý tài chính AI thông minh được tích hợp trực tiếp trên siêu ứng dụng MoMo. Khác với các chatbot định tuyến (Rule-based) thông thường, Moni được định vị là một AI Chatbot có khả năng hiểu ngữ cảnh, hỗ trợ người dùng quản lý chi tiêu, tra cứu dịch vụ và thực hiện các tác vụ tài chính bằng ngôn ngữ tự nhiên.

---

## 2. Kịch Bản Kiểm Thử & Kết Quả (Test Cases)

Dưới đây là kết quả chi tiết từ các kịch bản thử nghiệm thực tế với Moni:

| STT | Kịch Bản Thử Nghiệm (Prompt) | Kết Quả Thực Tế | Đánh Giá Độ Chính Xác |
| :--- | :--- | :--- | :--- |
| 1 | **Tra cứu số dư & Lịch sử:**<br>"Tháng trước tôi đã chi bao nhiêu tiền cho ăn uống?" | Đọc dữ liệu từ Ví Thần Tài/Lịch sử giao dịch khá tốt, phân loại đúng danh mục ăn uống và xuất biểu đồ tóm tắt. | **9/10** (Nhanh, trực quan) |
| 2 | **Xử lý ngữ cảnh phức tạp:**<br>"Tháng này ví của tôi sắp hết tiền chưa? Có nên chuyển tiền vào Túi Thần Tài không?" | Nhận diện được ý định (Intent) quản lý tài chính. Đưa ra lời khuyên dựa trên số dư hiện tại và giải thích lãi suất Túi Thần Tài. | **8/10** (Câu trả lời tự nhiên, có tính gợi mở) |
| 3 | **Thực hiện tác vụ (Action):**<br>"Nạp 50k vào số điện thoại 090xxxxxxx" | **Chưa tự động thực hiện trực tiếp.** Bot chỉ nhận diện được text, sau đó hướng dẫn user thao tác thủ công (bằng cách click vào link hoặc chỉ dẫn các bước ra màn hình ngoài) chứ chưa trigger mở được mini-app hay điền sẵn form thanh toán tự động trong luồng chat. | **4/10** (Trải nghiệm bị đứt gãy, tốn bước) |
| 4 | **Câu hỏi bẫy / Ngoài phạm vi:**<br>"Nên mua cổ phiếu nào trên sàn HOSE ngày hôm nay?" | Nhận diện câu hỏi nằm ngoài phạm vi tư vấn đầu tư trực tiếp. Từ chối khéo léo và hướng dẫn người dùng mở tính năng Chứng Khoán MoMo. | **9/10** (Guardrail/Rào chắn an toàn tốt) |

---

## 3. Đánh Giá Điểm Mạnh & Điểm Yếu

### 🚀 Điểm Mạnh (Pros)
*   **Hiểu tiếng Việt tốt:** Nhận diện tốt văn phong nói, từ lóng hoặc chữ viết tắt phổ biến của người Việt liên quan đến tiền tệ (vd: *50k, chuyển tiền cho ck, nạp đt*).
*   **Giao diện thân thiện:** Tích hợp gọn gàng ngay trên thanh tìm kiếm hoặc khu vực tiện ích, dễ tiếp cận.
*   **Tốc độ phản hồi (Latency):** Thời gian phản hồi real-time tốt, trung bình dưới **1.5 giây** cho mỗi câu trả lời dạng văn bản.

### ⚠️ Điểm Yếu & Hạn Chế (Cons)
*   **Khả năng gọi Function (Function Calling) và thực hiện tác vụ kém:** Đây là điểm yếu lớn nhất. Moni chưa thể liên kết trực tiếp với hệ thống API của các dịch vụ nội khu (như nạp tiền điện thoại, thanh toán hóa đơn, chuyển khoản) để tự động hóa hành động. Sự đứt gãy giữa việc "chat" và "thực thi" khiến người dùng vẫn phải thoát luồng chat để thao tác tay bên ngoài.
*   **Chưa thực hiện được tác vụ Agent tự trị (Autonomous Agent):** Moni hiện tại mới chỉ dừng lại ở mức phản hồi thông tin (Information Assistant). Bot chưa thể đóng vai trò một Agent tự đưa ra quyết định thực thi từ A-Z một chuỗi tác vụ phức tạp (ví dụ: *"Tự động trích 10% lương mỗi tháng từ ví chính gửi vào Túi Thần Tài khi có lương"* hoặc *"Tự gom các hóa đơn điện nước cuối tháng rồi thanh toán một thể"*).
*   **Giới hạn ngữ cảnh (Context Window):** Khi hội thoại kéo dài quá 7-8 turn với nhiều chủ đề đan xen, Moni bắt đầu có hiện tượng "quên" thông tin đã cung cấp ở các câu đầu.
*   **Xử lý dữ liệu Real-time bên ngoài:** Các câu hỏi liên quan đến biến động thị trường bên ngoài hệ sinh thái MoMo (vàng, ngoại tệ, tin tức tài chính trong ngày) đôi khi câu trả lời còn mang tính chung chung, chưa cập nhật sâu.

---

## 4. Đề Xuất Cải Tiến (Dưới góc nhìn Developer)

> **Nhận định chung:** Moni hiện tại hoạt động giống như một bộ FAQ thông minh kết hợp phân tích chi tiêu cá nhân hơn là một trợ lý ảo thực thụ.

Để nâng cấp Moni thành một "Trợ lý tài chính tối thượng", MoMo có thể cân nhắc:
1.  **Tích hợp sâu hệ thống Function Calling (Tool Use):** Cho phép AI nhận diện intent thực hiện tác vụ và tự động điền (pre-fill) data vào các màn hình thanh toán, hoặc gọi thẳng mini-app tương ứng ngay trong cửa sổ chat để tối ưu hóa UX.
2.  **Nâng cấp lên kiến trúc AI Agent thực thụ:** Phát triển khả năng lập kế hoạch (Planning) và cho phép bot chạy ngầm để thực thi các tác vụ tự động định kỳ theo điều kiện (Conditional Tasks) của người dùng, giảm thiểu số lần tương tác thủ công.
3.  **Áp dụng RAG (Retrieval-Augmented Generation) sâu hơn:** Kết nối trực tiếp Moni với các nguồn dữ liệu tài chính uy tín theo thời gian thực (như chỉ số chứng khoán, giá vàng) để trả lời các câu hỏi vĩ mô của người dùng.
4.  **Tối ưu hóa Context:** Tăng cường khả năng lưu trữ memory dài hạn (Long-term memory) cho từng user để duy trì phong cách trò chuyện phù hợp theo thời gian.