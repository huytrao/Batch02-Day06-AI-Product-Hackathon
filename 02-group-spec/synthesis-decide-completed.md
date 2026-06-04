# Toolkit - Evidence to Build Slice (Completed)

## 1. Gom evidence thanh cum

| Cum workflow/pain | Evidence lien quan | Ket luan product |
|---|---|---|
| Khong biet quan nao giao nhanh ngay luc nay | User phai mo Grab/ShopeeFood, Google Maps, Facebook group de doi chieu ETA va trang thai quan | Can mot flow hep "Giao nhanh trong 45 phut", khong can full directory. |
| Thong tin bi phan manh va mau thuan | ETA app, review, post cong dong va gio mo cua co the khac nhau | AI phai tong hop tin hieu va show source/confidence. |
| AI co the hallucinate neu khong co source | Evidence self-use: AI bia review, sai gia, sai menu chay | Guardrail: khong cite khi khong co source; confidence LOW khi du lieu yeu. |
| Failure khi quan dong/ship cham | Negative cases trong evidence plan va failure examples | Can fallback: call first, pickup, alternatives, correction report. |

## 2. Insight

```text
User cu dan Ocean Park 1 khong chi can danh sach quan an gan nha.
Ho that ra can ho tro ra quyet dinh nhanh va dang tin ve viec "nen dat quan nao ngay bay gio",
vi evidence cho thay thong tin mo cua, ETA, menu, gia va review bi phan manh/mau thuan, trong khi AI assistant co the tra loi qua tu tin neu khong bi rang buoc boi source.
```

## 3. Opportunity

```text
Co hoi la dung AI de tong hop va rank mot so it lua chon giao nhanh dua tren ETA app, report cong dong, trang thai mo cua va do moi cua source,
giup user chon 1 trong 2 option co kha nang giao trong 30-45 phut,
trong khi van kiem soat failure/risk bang confidence badge, source summary, warning, fallback action va correction flow.
```

## 4. Chon build slice

| Cau hoi | Danh gia cho Slice B - Fast Delivery Suggestion |
|---|---|
| User cu the chua? | Dat. Cu dan Ocean Park 1 ban ron, dang can dat do an nhanh. |
| Task du hep chua? | Dat. Mot click "Giao nhanh trong 45 phut" -> nhan 2 goi y. Demo duoc trong 3 phut. |
| AI decision ro chua? | Dat. AI rank quan theo ETA du doan va confidence. |
| Failure path ro chua? | Dat. Quan dong/ship cham/ETA mau thuan -> LOW confidence, fallback, report. |
| Co evidence khong? | Co evidence self-use, AI failure logs, va ke hoach thu thap source ngoai nhom. Can bo sung link/screenshot that trong Day 06. |

## 5. Quyet dinh

**Quyet dinh:** Giu domain "dining info tai Ocean Park 1" nhung giam scope manh ve mot flow duy nhat: Fast Delivery Suggestion.

## 6. Cau chot cuoi

```text
Dua tren self-use evidence, AI failure examples va ke hoach thu thap ETA/review/community posts,
nhom se build prototype slice "Fast Delivery Suggestion",
cho cu dan Ocean Park 1 ban ron,
de giai quyet pain mat thoi gian doi chieu nhieu nen tang khi can dat do an nhanh,
bang cach AI rank 2 lua chon co kha nang giao trong 30-45 phut va giai thich bang confidence/source,
va se test failure path AI de xuat quan dong, ETA mau thuan, hoac delivery tre.
```

## 7. Backlog

- Live scraping tu Grab/ShopeeFood/Google Maps/Facebook.
- Payment va automatic order placement.
- Full search engine cho moi mon, moi cuisine, moi khu vuc.
- Dietary-safe recommendation cho chay/halal voi claim chac chan.
- He thong verification cong dong day du.
