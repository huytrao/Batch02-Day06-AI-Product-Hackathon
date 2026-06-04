# Template — Evidence Pack

Nộp kèm thin SPEC cuối Day 05.

## 1. Nhóm và track

**Tên nhóm:**  
**Track:** AI Product / Software Development  
**Product/app đã chọn:** Hệ thống hỗ trợ tìm kiếm ẩm thực thông minh tại Vinhomes Ocean Park 1 (OCP1)  
**Build slice đang nghĩ:** Một Agent thông minh tự động thu thập, tổng hợp thông tin quán ăn và giá cả tại OCP1 từ nhiều nguồn dữ liệu khác nhau.  

## 2. Self-use evidence

Nhóm tự dùng app/workflow và ghi lại điểm gãy.

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Mỗi khi muốn đi ăn thường phải lên Google Maps xem đánh giá và lướt ảnh chụp menu để tìm giá bán thực tế của sản phẩm. | | Low-confidence | Thông tin giá cả trên Google Maps thường bị phân mảnh, nằm rải rác trong ảnh chụp của khách hàng và không được cập nhật liên tục. |
| Phải chuyển đổi qua lại giữa nhiều nền tảng (Google Maps, Facebook Groups, TikTok) để đối chiếu thực đơn và không gian quán. | | Failure | Quy trình tìm kiếm thủ công qua nhiều nguồn gây tốn thời gian và dễ làm người dùng bỏ cuộc giữa chừng. |

## 3. User / review / social evidence

Nguồn có thể là review App Store/Play, group, comment, phỏng vấn nhanh, hoặc nguồn public khác.

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Mỗi lần sang OCP1 chơi muốn tìm quán ăn có giá cả rõ ràng khó quá, thông tin trên mạng chỗ thì cũ, chỗ thì không có menu." | Thảo luận cộng đồng cư dân OCP1 | Khách du lịch / Người ngoài khu đô thị | Thiếu thông tin minh bạch về giá cả và thực đơn trước khi đến quán. |
| "Nhiều quán ăn ở đây thay đổi giá hoặc có phụ thu nhưng không cập nhật trên fanpage, đến nơi tính tiền mới biết." | Review trong nhóm ẩm thực | Cựu thành viên / Cư dân tại OCP1 | Gặp rủi ro về sai lệch thông tin chi phí thực tế (Asymmetric information). |

Nếu chưa có nguồn ngoài nhóm, ghi rõ:

```text
Dữ liệu trên dựa trên trải nghiệm thực tế của các thành viên và phỏng vấn nhanh một số người dùng thường xuyên tìm kiếm địa điểm ăn uống tại OCP1. Nhóm sẽ kiểm chứng lại bằng khảo sát diện rộng trước checkpoint M1 Day 06.
```
## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| Google Maps / Foody | Hiển thị thông tin quán ăn dựa trên định vị, đi kèm phần hình ảnh do người dùng đóng góp và menu (nếu có). | Tập trung dữ liệu đánh giá và hình ảnh thực tế từ cộng đồng. | Có, áp dụng phần trích xuất thông tin cốt lõi (tên quán, địa chỉ, khoảng giá). |

## 5. Evidence -> Insight

```text
Evidence nổi bật nhất:
Người dùng phải truy cập Google Maps, lướt qua hàng chục đánh giá và ảnh chụp thủ công chỉ để tìm kiếm và xác nhận giá bán chính xác của món ăn trước khi quyết định đến quán.

Insight:
User không chỉ gặp tình trạng mất thời gian lướt ảnh tìm menu.
Thật ra họ cần một nơi uy tín để tìm kiếm quán ăn theo đúng ý thích do khu vực Ocean Park 1 quá rộng lớn, nhiều quán ăn bị che khuất bởi các tòa nhà cao tầng khiến việc tìm kiếm thực tế hoặc định vị bản đồ thông thường gặp khó khăn. Họ cần hỗ trợ đưa ra quyết định nhanh dựa trên các bộ lọc cụ thể như: tìm món nước, tìm quán ăn giá rẻ, hay tìm đích danh những quán bán đặc sản của khu vực.

Opportunity:
AI có thể giúp bằng cách sử dụng một Agent tự động quét, cào dữ liệu đa nguồn để tổng hợp, định vị chính xác và phân loại các quán ăn tại OCP1 theo đúng khẩu vị, khoảng giá và phân khúc món ăn mà người dùng yêu cầu.
```

## 6. Evidence đổi SPEC như thế nào?

- [ ] Đổi user chính.
- [ ] Đổi pain statement.
- [x] Đổi build slice.
- [ ] Đổi Auto/Aug decision.
- [ ] Đổi 4 paths.
- [ ] Đổi failure mode.
- [ ] Đổi owner/test plan.

Ghi rõ 1-2 thay đổi quan trọng:

```text
Trước evidence, nhóm định xây dựng một ứng dụng danh bạ địa điểm ăn uống thông thường tại OCP1.
Sau evidence, nhóm đổi thành phát triển một Agent đa nguồn tập trung sâu vào việc bóc tách dữ liệu giá cả, thực đơn và phân loại quán theo nhu cầu cụ thể (món nước, giá rẻ, cơm tấm,...).
Lý do: Địa bàn OCP1 rộng và bị che khuất bởi nhiều tòa nhà cao tầng, bộ lọc thông thường không giải quyết được nhu cầu tìm kiếm nhanh một địa điểm uy tín đúng gu của người dùng.
```
