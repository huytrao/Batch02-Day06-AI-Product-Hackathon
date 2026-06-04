# Evidence Pack - Ocean Park 1 Eats

## 1. Nhom va track

**Ten nhom:** TBD - Ocean Park 1 Eats Team  
**Track:** AI Product / Software Development  
**Product/app da chon:** Ocean Park 1 Eats - he thong ho tro tim va chon quan an quanh Vinhomes Ocean Park 1 bang thong tin tong hop da nguon.  
**Build slice dang nghi:** Fast Delivery Suggestion - AI rank 2 quan co kha nang giao nhanh trong 30-45 phut, kem ETA, confidence, ly do, source summary va fallback.

## 2. Self-use evidence

| Observation | Screenshot/link | Path lien quan | Dieu hoc duoc |
|---|---|---|---|
| Khi muon dat do an nhanh, user thuong phai mo nhieu nguon: Facebook group, Google Maps, Grab/ShopeeFood. | Self-use note, can bo sung screenshot Day 06 | Happy / Low-confidence | Search cost la pain chinh; can flow tra 2 option. |
| AI goi y quan co mon chay nhung thuc te khong phu hop nguoi an chay nghiem ngat. | https://gemini.google.com/share/70129533832a | Failure / Correction | Khong claim menu neu thieu source. |
| AI bia review 1-2 sao voi ten nguoi dung va noi dung chi tiet. | https://gemini.google.com/share/b2261087abb0 | Failure / Correction | Khong duoc bia evidence; can source summary. |
| AI goi y sai muc gia cua quan com tho trong 2 session. | https://gemini.google.com/share/51b3e9d4ca94 va https://gemini.google.com/share/89b5e6a8ad09 | Low-confidence / Failure / Correction | Khi du lieu yeu, confidence phai LOW. |

## 3. User / review / social evidence

| Quote / review / observation | Nguon | User la ai? | Pain/failure mode |
|---|---|---|---|
| "Muon an nhanh nhung phai xem ca app giao hang lan group cu dan vi ETA tren app chua chac dung luc cao diem." | Gia dinh evidence can kiem chung bang FB/community post | Cu dan OCP1 dat do an luc trua/toi | ETA mau thuan, search cost cao. |
| "Quan tren Maps van mo nhung app giao hang khong nhan don hoac bao qua lau." | Gia dinh negative case can kiem chung bang screenshot | Cu dan/nguoi lam viec quanh OCP1 | Open status khong dong nghia co delivery. |

```text
Mot phan evidence social hien la gia dinh dua tren self-use va quan sat cua nhom. Truoc checkpoint M1 Day 06, Research Owner can kiem chung bang it nhat 10 post/comment cong khai trong group cu dan OCP1, 5 Google Maps snippets va 10 ETA rows tu Grab/ShopeeFood hoac sample controlled data co screenshot.
```

## 4. Competitor / analog evidence

| App / mo hinh tham khao | Ho xu ly task nay the nao? | Pattern hoc duoc | Co ap dung trong 1 ngay khong? |
|---|---|---|---|
| GrabFood / ShopeeFood | Hien nha hang, menu, phi ship va ETA theo nen tang rieng. | ETA quan trong nhung chi la 1 source. | Co. Dung fake/controlled ETA rows. |
| Google Maps | Hien gio mo cua, review, anh menu va vi tri. | Huu ich cho open status/review, yeu cho delivery now. | Co. Luu source label va timestamp. |
| Facebook resident groups | Bao cao gan thoi gian thuc ve quan dong, ship cham, mon ngon. | Community signals giup phat hien conflict. | Co. Dung curated posts/comments hoac mock labels. |

## 5. Evidence -> Insight

```text
Evidence noi bat nhat:
User khong chi mat thoi gian tim quan, ma con phai tu danh gia do tin cay cua nhieu nguon mau thuan. Evidence self-use cho thay AI assistant co the sai gia, sai menu va tham chi bia review khi khong co source.

Insight:
User khong chi gap surface problem la "khong biet an gi".
That ra ho can decision support dang tin cho cau hoi hep: "nen dat quan nao co kha nang giao nhanh ngay bay gio?"

Opportunity:
AI co the giup bang cach tong hop/rank cac tin hieu ETA, open status, community report va prep-speed tag de de xuat 2 option giao nhanh.
```

## 6. Evidence doi SPEC nhu the nao?

- [ ] Doi user chinh.
- [x] Doi pain statement.
- [x] Doi build slice.
- [x] Doi Auto/Aug decision.
- [x] Doi 4 paths.
- [x] Doi failure mode.
- [x] Doi owner/test plan.

```text
Truoc evidence, nhom dinh xay dung mot Agent/danh ba am thuc da nguon cho OCP1.
Sau evidence, nhom doi thanh slice hep "Fast Delivery Suggestion": AI chi rank 2 lua chon co kha nang giao nhanh trong 30-45 phut.
Ly do: Evidence cho thay rui ro lon nhat la thong tin sai/hallucination va user mat thoi gian doi chieu.
```
