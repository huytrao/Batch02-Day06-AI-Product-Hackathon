# Workshop — Mổ App AI Thật  
## Finding note + sketch as-is / to-be

**Sản phẩm chọn:** MoMo — Moni  
**AI feature:** Trợ thủ tài chính / chatbot trong app MoMo  
**Output:** finding note + sketch as-is / to-be  
**Finding chính:** Moni đang trả lời thì dừng giữa chừng, nhưng không có recovery path rõ ràng.

---

## 1. Promise vs Reality

### Product hứa gì?

Moni được đặt trong MoMo như một trợ thủ AI hỗ trợ người dùng trong app tài chính. Người dùng kỳ vọng có thể hỏi bằng ngôn ngữ tự nhiên và nhận được hỗ trợ nhanh, rõ ràng, thay vì phải tự tìm trong nhiều màn hình.

### User nào được hứa sẽ được giúp?

User chính là người dùng MoMo có nhu cầu:

- Hỏi nhanh về giao dịch hoặc chi tiêu.
- Cần được hướng dẫn thao tác trong app.
- Muốn hiểu thông tin tài chính cá nhân.
- Không muốn tự tìm trong nhiều màn hình.
- Cần một trợ lý trả lời dễ hiểu và đáng tin.

### Tôi kỳ vọng AI làm được task nào?

Task kỳ vọng:

> Người dùng hỏi một câu liên quan đến chi tiêu hoặc thao tác tài chính, Moni trả lời đầy đủ, rõ ràng, và nếu không chắc thì hỏi lại hoặc đưa lựa chọn tiếp theo.

Ví dụ input dùng để test:

```text
Tháng này tôi tiêu nhiều nhất vào khoản nào?
```

Hoặc:

```text
Tôi muốn biết gần đây mình chi tiêu nhiều ở đâu. Hãy phân tích giúp tôi.
```

### Khi dùng thật, điểm gãy xuất hiện ở đâu?

Điểm gãy xuất hiện ở giai đoạn Moni đang sinh câu trả lời:

```text
User nhập câu hỏi
→ Moni bắt đầu trả lời
→ Câu trả lời dừng giữa chừng
→ Không có thông báo lỗi rõ ràng
→ Không có nút tiếp tục
→ User không biết phải làm gì tiếp
```

Đây là điểm gãy trong workflow vì người dùng đã bắt đầu tin rằng AI đang xử lý được yêu cầu, nhưng cuối cùng lại không nhận được câu trả lời hoàn chỉnh.

---

## 2. Evidence

### Observation tự dùng

> Moni đang trả lời thì dừng giữa chừng. Câu trả lời không hoàn tất và không có hướng dẫn rõ ràng để tiếp tục.

### Hành vi quan sát được

```text
Moni bắt đầu phản hồi
→ Nội dung trả lời bị dừng
→ Không thấy kết luận cuối cùng
→ Không thấy nút “Tiếp tục”
→ Không thấy nút “Tạo lại câu trả lời”
→ User phải tự hỏi lại hoặc thoát ra
```

### Screenshot

Chèn screenshot vào đây khi nộp bài:

```text
[Chèn screenshot Moni bị dừng giữa chừng]
```

Nếu không có screenshot, evidence tối thiểu có thể ghi là:

```text
Evidence: observation khi self-use — Moni đang trả lời thì dừng giữa chừng, không có UX recovery rõ ràng.
```

---

## 3. Bốn paths

| Path | Quan sát / đánh giá |
|---|---|
| Happy path | Khi Moni hiểu câu hỏi và trả lời bình thường, user nhận được phản hồi nhanh trong cùng giao diện chat. Đây là trạng thái tốt nhất: user hỏi → Moni trả lời → user có thể tiếp tục hỏi. |
| Low-confidence path | Chưa thấy cơ chế rõ ràng cho trường hợp Moni không chắc. Nếu thiếu thông tin, hệ thống nên hỏi lại hoặc đưa options, nhưng path này chưa nổi bật trong trải nghiệm quan sát được. |
| Failure path | Failure chính là Moni đang trả lời thì dừng giữa chừng. User không biết đây là lỗi mạng, lỗi AI, thiếu dữ liệu hay câu trả lời đã kết thúc. |
| Correction path | Khi user muốn sửa hoặc yêu cầu Moni tiếp tục, chưa thấy correction được lưu/log rõ ràng. User có thể phải nhập lại câu hỏi từ đầu. |

---

## 4. Finding viết thành product decision

### Trigger

Khi user hỏi Moni một câu cần phản hồi đầy đủ, ví dụ:

```text
Tháng này tôi tiêu nhiều nhất vào khoản nào?
```

### Failure

AI/product bắt đầu trả lời nhưng dừng giữa chừng. Sau khi dừng, sản phẩm không hiển thị trạng thái lỗi, không cho user tiếp tục câu trả lời và không có lựa chọn phục hồi.

### Impact

Hậu quả là user không nhận được câu trả lời hoàn chỉnh, không biết có nên tin phần nội dung đã hiện ra hay không, và không biết hành động tiếp theo là gì. Trong bối cảnh app tài chính, điều này làm giảm niềm tin vì user đang hỏi về thông tin liên quan đến tiền, chi tiêu hoặc giao dịch.

### Layer lỗi

Lỗi thuộc các layer:

- **UX Recovery:** không có cách phục hồi khi câu trả lời bị dừng.
- **Failure Handling:** không báo rõ lỗi hoặc trạng thái gián đoạn.
- **Trust:** user không biết câu trả lời dang dở có đáng tin không.
- **Workflow Continuity:** user phải tự hỏi lại hoặc thoát flow.

### Product decision

> Khi Moni bị gián đoạn trong lúc trả lời, sản phẩm không được để người dùng bị kẹt. Cần có cơ chế UX recovery gồm: trạng thái lỗi rõ ràng, nút **Tiếp tục trả lời**, nút **Tạo lại câu trả lời**, nút **Gặp hỗ trợ**, và lưu lại phần nội dung đã sinh để người dùng có thể tiếp tục từ điểm bị dừng.

---

## 5. Requirement đề xuất

Khi câu trả lời bị gián đoạn, Moni cần:

1. Hiển thị trạng thái: **“Câu trả lời chưa hoàn tất.”**
2. Có nút **Tiếp tục trả lời**.
3. Có nút **Tạo lại câu trả lời**.
4. Có nút **Gặp hỗ trợ** nếu lỗi lặp lại.
5. Lưu lại phần câu trả lời đã sinh.
6. Ghi log lỗi để đội sản phẩm biết câu hỏi nào làm Moni bị dừng.

---

## 6. Sketch as-is / to-be

### As-is flow

```text
┌──────────────────────┐
│ User mở MoMo          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ User vào Moni         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ User nhập câu hỏi     │
│ "Tháng này tôi tiêu   │
│ nhiều nhất ở đâu?"    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Moni bắt đầu trả lời  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Câu trả lời dừng      │
│ giữa chừng            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ User bị kẹt           │
│ Không biết làm gì     │
└──────────────────────┘
```

**Điểm gãy:**  
Moni dừng giữa chừng nhưng không có recovery path.

---

### To-be flow

```text
┌──────────────────────┐
│ User mở MoMo          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ User vào Moni         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ User nhập câu hỏi     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Moni bắt đầu trả lời  │
└──────────┬───────────┘
           ↓
┌─────────────────────────────┐
│ Hệ thống kiểm tra trạng thái │
│ sinh câu trả lời             │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ Nếu trả lời hoàn tất:        │
│ → Show answer                │
│ → Gợi ý next action          │
└─────────────────────────────┘

Nếu bị dừng:
           ↓
┌─────────────────────────────┐
│ Hiện message:                │
│ "Câu trả lời chưa hoàn tất"  │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ Button: Tiếp tục trả lời     │
│ Button: Tạo lại câu trả lời  │
│ Button: Gặp hỗ trợ           │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│ Lưu phần nội dung đã sinh    │
│ Ghi log lỗi để cải thiện     │
└─────────────────────────────┘
```

**Path đã sửa:**  
Failure path được chuyển thành recovery path có hành động rõ ràng cho user.

---

## 7. Câu đưa vào SPEC

> Nếu Moni bị gián đoạn trong lúc sinh câu trả lời, hệ thống phải hiển thị trạng thái “Câu trả lời chưa hoàn tất”, giữ lại phần nội dung đã sinh, cung cấp các hành động “Tiếp tục trả lời”, “Tạo lại câu trả lời”, “Gặp hỗ trợ”, và ghi log câu hỏi gây lỗi để đội sản phẩm kiểm tra lại.

---

## 8. Test case đề xuất cho SPEC

### Test case 1: Câu trả lời dài bị dừng

**Input:**

```text
Hãy phân tích chi tiêu tháng này của tôi theo từng nhóm và đưa ra gợi ý tiết kiệm.
```

**Expected behavior:**

```text
Nếu Moni trả lời đầy đủ:
→ Show answer hoàn chỉnh.

Nếu Moni bị dừng:
→ Show “Câu trả lời chưa hoàn tất.”
→ Show button “Tiếp tục trả lời.”
→ Show button “Tạo lại câu trả lời.”
→ Không xóa phần trả lời đã có.
```

### Test case 2: User bấm “Tiếp tục trả lời”

**Action:**

```text
User bấm “Tiếp tục trả lời”
```

**Expected behavior:**

```text
Moni tiếp tục từ ý đang bị dừng, không bắt đầu lại từ đầu.
```

### Test case 3: User bấm “Tạo lại câu trả lời”

**Action:**

```text
User bấm “Tạo lại câu trả lời”
```

**Expected behavior:**

```text
Moni tạo lại câu trả lời mới, có thể ngắn hơn hoặc chia thành từng bước.
```

### Test case 4: Lỗi lặp lại

**Condition:**

```text
Moni bị dừng 2 lần trong cùng một câu hỏi.
```

**Expected behavior:**

```text
Hiển thị lựa chọn “Gặp hỗ trợ” hoặc “Báo lỗi”.
```

---

## 9. Checklist tự kiểm trước khi nộp

- [x] Có observation cụ thể: Moni đang trả lời thì dừng giữa chừng.
- [x] Có prompt/input để test.
- [x] Có đủ 4 paths: happy, low-confidence, failure, correction.
- [x] Finding được viết thành product decision.
- [x] Sketch có as-is và to-be.
- [x] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.
- [ ] Cần bổ sung screenshot thật từ app nếu giáo viên bắt buộc phải có ảnh.

---
https://cdn.discordapp.com/attachments/1510868202140336214/1511591873129611284/9D8643DE-6A1F-41C1-AE73-E8D68F48FCF5.png?ex=6a210322&is=6a1fb1a2&hm=cd243267e5d7eed4ac7e9d8d8415dae9324837ad14cf5b5638ca65e873d20e64&

## 10. Kết luận

Finding quan trọng nhất không phải là “Moni trả lời hay hay dở”, mà là workflow bị gãy khi Moni đang trả lời thì dừng giữa chừng. Đây là lỗi nghiêm trọng vì người dùng không nhận được câu trả lời hoàn chỉnh và không có cách phục hồi rõ ràng.

Vì vậy, quyết định product cần đưa vào SPEC là thiết kế một failure recovery path cho Moni. Khi AI bị dừng, hệ thống phải nói rõ trạng thái, giữ lại phần nội dung đã sinh, cho phép tiếp tục hoặc tạo lại câu trả lời, và có đường chuyển sang hỗ trợ nếu lỗi lặp lại.

Một sản phẩm AI tốt không chỉ cần xử lý tốt happy path, mà còn phải giúp user recover khi AI sai, không chắc, hoặc bị gián đoạn.
