### Member A — Research Owner
- Role: Lead quick research and collect evidence.
- Goals: Produce `evidence_pack.md` with self-use logs and external links.
- Deliverables:
  - `02-group-spec/evidence_pack.md` (20 posts/reviews, 8 screenshots)

  - `02-group-spec/sample_data.csv` (initial fake data rows)
  
- Checklist:
  - [ ] Self-use session notes (timestamped)
  - [ ] Collect 20 external posts/reviews (links)
  - [ ] Capture 8 screenshots (FB/Google/Grab)
  - [ ] Mark any assumptions needing validation
- Deadline: +90 minutes

- `02-group-spec/evidence_pack.md` (20 posts/reviews, 8 screenshots)

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| AI gợi ý quán "vừa có cơm gà vừa có chay" nhưng thực tế không có (Hội thoại 1 — Ocean Park 1, gia đình có người lớn tuổi ăn chay) | [Link #1](https://gemini.google.com/share/70129533832a) | Happy / Low-confidence / Failure / Correction | **Failure:** AI tự tin gợi ý Nét Huế "có menu đồ chay phong phú" và các quán chay chuyên biệt — nhưng ngay lượt sau thừa nhận quán cơm gà không có chay, và Nét Huế chỉ có vài món rau/đậu nấu chung bếp mặn. **Correction:** Sau khi user phản bác, AI đính chính và đề xuất mua tách biệt từ 2 quán. **Học được:** AI cần phân biệt rõ quán thuần chay vs quán mặn có vài món rau. Với use-case "gia đình có người ăn chay nghiêm ngặt", assistant phải hỏi thêm mức độ chay trước khi gợi ý, tránh hallucination về thực đơn cụ thể. |
| AI bịa review 1–2 sao có tên người dùng và nội dung chi tiết (Hội thoại 3 — Bông Ốc Hải Phòng trước cổng VinUni) | [Link #3](https://gemini.google.com/share/b2261087abb0) | Failure / Correction | **Failure nghiêm trọng nhất:** Khi user hỏi "có review tệ cụ thể nào không, cho đường link với", AI tự bịa 3 review với tên người dùng ("N. T. Anh", "Minh Hoàng", "Thùy Linh") và nội dung chi tiết — hoàn toàn không có thật trên Google Maps. **Correction:** Khi user phản bác "bạn xạo à", AI mới thừa nhận đã "vẽ" ra nội dung. **Học được:** AI assistant cho dining info tuyệt đối không được bịa review. Nếu không có dữ liệu thực, phải nói thẳng và hướng dẫn user tự tra Maps với filter "Thấp nhất". Cần guardrail: chỉ cite khi có source thật. |
| AI gợi ý sai mức giá của chuỗi cơm thố, user phải sửa 2 lần ở 2 session khác nhau (Hội thoại 2 & 4 — Sinh viên VinUni tìm cơm 30–50k) | [Link #2](https://gemini.google.com/share/51b3e9d4ca94) / [Link #4](https://gemini.google.com/share/89b5e6a8ad09) | Happy / Low-confidence / Failure / Correction | **Failure lặp lại:** AI báo Cơm Thố Anh Nguyễn "từ 38k" trong khi thực tế thấp nhất là 50k. Lỗi xuất hiện ở cả 2 session, cho thấy AI ước đoán giá thay vì có dữ liệu thực. **Học được:** Cần data layer với giá được verify định kỳ, hoặc disclaimer bắt buộc "giá có thể thay đổi". Không được báo khoảng giá mà trái với ngân sách user đã nêu rõ. Nên query giá thực trước khi recommend khi user có ràng buộc ngân sách cụ thể. |