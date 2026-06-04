# Thin SPEC Cuoi Day 05 - Ocean Park 1 Eats

## 1. Track, product/app va user

**Track:** AI Product / Software Development  
**Product/app that te:** Ocean Park 1 Eats - Aggregated Dining Info cho cu dan Vinhomes Ocean Park 1  
**User cu the:** Cu dan Ocean Park 1 ban ron, dang can dat do an giao nhanh trong khoang 30-45 phut.  
**Nhom co phai user that khong? Neu khong, khac o dau?**  
Mot so thanh vien co trai nghiem tim quan an/order quanh Ocean Park 1 hoac tuong tu khu do thi lon. Neu khong phai cu dan OCP1 thuong tru, nhom can kiem chung bang self-use logs, FB/community posts, Google Maps va ETA tren Grab/ShopeeFood.

## 2. Evidence summary

| Evidence | Nguon | User/pain noi len dieu gi? | SPEC phai doi gi? |
|---|---|---|---|
| User phai mo Google Maps, Facebook group, Grab/ShopeeFood de doi chieu gio mo cua, menu, gia va ETA. | Self-use + `idea_description_project.md` | Pain la quyet dinh cham vi thong tin phan manh. | Cat scope thanh "Giao nhanh trong 45 phut". |
| AI dining assistant co the sai mon chay, sai gia, hoac bia review khi thieu source. | `evidence.md` va cac Gemini links | Trust la rui ro lon. | Moi card phai co confidence, source summary va warning. |
| ETA va open status co the mau thuan giua app, Maps va cong dong. | Ke hoach thu thap FB/Maps/Grab/ShopeeFood | User can goi y nho nhung giai thich duoc. | Output chi gom 2 quan duoc rank. |

## 3. Pain statement

```text
User cu dan Ocean Park 1 ban ron dang gap kho o buoc chon quan de dat do an giao nhanh,
vi thong tin ETA, gio mo cua, menu va review bi phan manh tren Facebook, Google Maps, Grab/ShopeeFood va cac bao cao cong dong,
dan toi viec mat thoi gian doi chieu, chon sai quan, hoac dat nham quan giao cham/dong cua.
Bang chung chinh la self-use workflow phai mo nhieu nen tang va cac failure trong evidence: AI goi y sai gia, sai menu chay, hoac bia review khi khong co nguon that.
```

## 4. Build slice

```text
Cho cu dan Ocean Park 1 ban ron dang can dat do an giao nhanh trong 30-45 phut,
prototype se dung AI de rank 2 quan co kha nang giao nhanh dua tren ETA app, bao cao cong dong, trang thai mo cua va tag toc do chuan bi,
tao ra 2 recommendation cards co ETA du doan, confidence, ly do, source summary va fallback action,
va xu ly failure "quan dong/ship cham/du lieu mau thuan" bang warning, call-first, goi y pickup/alternative va report wrong info.
```

## 5. Auto/Aug decision

- [x] **Augmentation:** AI goi y/draft/phan loai, user quyet cuoi.
- [ ] **Conditional automation:** AI tu lam trong case hep; case mo ho/rui ro chuyen nguoi.
- [ ] **Automation:** AI tu quyet va tu hanh dong.

**Ly do chon:** AI chi nen rank va giai thich, khong duoc dat hang hoac noi chac ve ETA.  
**Human role:** decider + rescuer + trainer. User quyet dinh dat/call/pickup; Evidence Owner review correction.

## 6. Four paths

| Path | Prototype phai the hien gi? |
|---|---|
| Happy | User bam "Giao nhanh trong 45 phut"; he thong tra 2 card co ETA 30-40 phut, HIGH/MEDIUM confidence, ly do ngan va source summary. |
| Low-confidence | ETA app va report cong dong mau thuan; card hien LOW confidence, warning "Check before ordering", fallback "Call vendor / choose pickup". |
| Failure | Quan duoc goi y nhung thuc te dong/khong giao/tre >60 phut; UI cho phep report, ha confidence trong session, hien 2 lua chon thay the. |
| Correction | User bam "Report wrong info"; system tao verification ticket va khong de xuat high-confidence cho quan do trong session. |

## 7. Failure mode nguy hiem nhat

```text
Neu user dang doi va tin vao goi y "giao nhanh",
AI co the de xuat mot quan thuc te da dong, khong nhan delivery, hoac ETA that >60 phut,
hau qua la user mat thoi gian, co the mat tien/khong dat duoc mon, va mat niem tin vao san pham.
Prototype se xu ly bang confidence badge, source timestamp, canh bao khi du lieu cu/mau thuan, nut Call first, fallback alternatives va report wrong info.
Owner kiem thu path nay la Trao An Huy (2A202600819) - Member E / Demo & Repo Owner.
```

## 8. Owner plan cho sang Day 06

| Thanh vien | Viec phu trach | Bang chung can co trong repo |
|---|---|---|
| Le Huu Dat (2A202600630) - Member A | Research / evidence | Self-use logs, 10+ FB/community observations, 5+ Google Maps snippets, 10+ ETA rows. |
| Nguyen Dong Anh (2A20600760) - Member B | SPEC evidence synthesis | Evidence summary, opportunity statement, source freshness assumptions. |
| Cong Thai (2A202600949) - Member C | SPEC | `build_slice.md`, AI decision rules, four paths, guardrails. |
| Nguyen Duc Manh (2A20260724) - Member D | Prototype | Minimal UI flow, SQLite/CSV schema, recommendation heuristic, sample data. |
| Trao An Huy (2A202600819) - Member E | Test / failure path + demo script / repo | HP/LC/FP/CP test cases, 3-minute demo script, README check. |
