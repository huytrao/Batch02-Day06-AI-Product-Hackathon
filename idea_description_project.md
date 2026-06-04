# description.md — Ocean Park 1 — Aggregated Dining Info

## 1. Problem Statement
Residents of Ocean Park 1 struggle to find reliable, up-to-date information about nearby food options because relevant information is scattered across Facebook groups, Google Maps, ShopeeFood, GrabFood and ad-hoc user reports. This causes wasted time, wrong expectations (hours/menu/availability), and low trust when ordering or visiting.

## 2. Evidence Pack

### Self-use Evidence (observations to record)
- Not sure what to eat today; many suggestions duplicate the same places.
- Too many Facebook posts; hard to filter verified recommendations.
- Unsure if a restaurant is open right now.
- Hard to find vegetarian/halal options quickly.
- Unclear delivery time expectations (ShopeeFood/Grab estimates vary).

### External Evidence (sources to collect)
- Facebook Group posts / comment threads (search: "Ocean Park ăn", "Ocean Park quán").
- Google Maps reviews filtered by recency and keywords ("mở", "giao", "chậm").
- ShopeeFood / GrabFood listing reviews and delivery ETA complaints.
- Local community chat logs or Telegram/Line (if available).
- Local TikTok / short videos mentioning restaurants.

Search keywords: "Ocean Park ăn gì", "Ocean Park quán mở không", "giao nhanh", "đóng cửa".

### Evidence Summary
- Repeated patterns: difficulty knowing whether a place is open right now; many subjective reviews; duplicate posts in FB group; delivery ETA complaints.  
- Less frequent: complaints about food safety (rare), price disputes (sporadic).

## 3. Opportunity Statement

User: Residents of Ocean Park 1 who want a quick, reliable decision on where to eat or order.  
Pain: They spend time scanning multiple platforms to check availability, type of food, and likely delivery time.  
Existing behavior: Ask in Facebook group, check Google Maps hours, open ShopeeFood/Grab for menus and delivery.  
Opportunity: Provide a compact, trustable summary (open now / cuisine / delivery ETA / verified by community) assembled from multiple sources, with clear confidence and easy recovery when information is uncertain.

Opportunity statement: For Ocean Park 1 residents who need a quick meal decision, our product aggregates local signals (social, maps, delivery platforms, user reports) to surface 2–3 recommended options with availability and confidence, reducing search time and failed orders.

## 4. Build Slice (3 options + chosen)

Slice A — Quick Open+Cuisine Finder
Cho: Resident cần biết quán nào đang mở trong 30 phút tới.  
Prototype dùng AI để aggregate giờ mở từ Google + posts + user reports and infer "open now" confidence.  
Output: Top 3 places "open now" with confidence score and one-sentence reason.  
Failure mitigation: show sources + suggest call number or human verification.

Slice B — Fast Delivery Suggestion (Chosen)
Cho: Resident muốn order nhanhest delivery within 30–45 min.  
Prototype dùng AI để combine delivery ETA signals from ShopeeFood/Grab + recent delivery reports to predict expected delivery time and recommend 2 options.  
Output: 2 recommended restaurants with predicted ETA + confidence + short note ("có sẵn món giao nhanh").  
Failure mitigation: show alternative pickup options and fallback to user confirmation.

Slice C — Dietary Filtered Suggest
Cho: Resident cần ăn chay/halal.  
Prototype dùng AI để filter aggregated sources for menu tags and community verification.  
Output: Top 3 verified vegetarian/halal-friendly places with evidence.  
Failure mitigation: show source quotes and allow user correction.

Chosen for Day 06 (most feasible in 6h): Slice B — Fast Delivery Suggest. Reason: narrow task, clear input signals from delivery platforms, high demo value, minimal data needed and easy to simulate with fake data and SQLite.

## 5. Auto / Aug Decision
- Decision: Conditional automation with strong augmentation.  
- AI role: predict delivery likelihood & ETA and propose 2 suggested options (AI suggests).  
- Human role: user reviews suggestions and confirms order (user decides).  
- Reason: delivery decisions have moderate risk (late delivery); show sources and require user confirmation to avoid harmful automation.

## 6. Four Paths (for Slice B)

Happy Path
- User asks "Giao nhanh" → AI aggregates recent ETAs and availability → suggests 2 options with ETA ~30–40 min and confidence high → user taps to view menu and orders.

Low Confidence Path
- AI finds conflicting ETA signals → shows suggestions with "low confidence" badge, lists sources, asks user to confirm if they want to call or order anyway.

Failure Path
- AI predicts fast delivery but actual ETA >60 min (delivery failure) → prototype logs mismatch and shows apology + alternative nearby options + option to cancel or call vendor.

Correction Path
- User reports wrong info (e.g., closed) → user submits correction form → system updates local cache and shows updated suggestion; owner flagged review for evidence owner.

## 7. Failure Mode
- Worst failure: AI recommends a restaurant as "fast delivery" but the place is closed or has no delivery (user loses time/money).  
Impact: user frustration, loss of trust, potential charge dispute.  
Prototype handling: always show evidence & sources, display confidence, provide quick fallback actions (call, view menu, alternative suggestions).  
Fallback when AI uncertain: mark suggestion as "check" and require user confirmation before ordering.

## 8. Owner Plan (high level)
- Research Owner: collect self‑use and external evidence (Facebook posts, Google Maps snippets, delivery ratings).  
- Evidence Owner: synthesize evidence->insight and produce opportunity statement.  
- Product Spec Owner: create build_slice.md + four paths + Auto/Aug decision.  
- Prototype Owner: prepare thin spec, inputs/outputs, demo flow, fake-data schema and SQLite sample.  
- Demo & Repo Owner: assemble description.md, repo structure, final thin SPEC and 3‑minute demo script.

## 9. Thin SPEC (Slice B — Fast Delivery Suggest)

Problem
- Residents cannot reliably identify restaurants that will deliver fast now; checking multiple apps is slow.

User
- Segment: Busy Ocean Park 1 residents wanting food delivered within ~45 minutes.

Workflow
1. User opens prototype and selects "Giao nhanh" and location.  
2. Prototype queries aggregated dataset (delivery ETAs, recent delivery reports, availability).  
3. AI ranks candidates and returns 2 suggestions with ETA and confidence.  
4. User inspects sources and confirms order (redirect to delivery app or view menu).

AI Decision
- Predict expected delivery time and confidence score per vendor+restaurant combo using heuristics over scraped ETA fields and recent reports.

Inputs
- Location (Ocean Park 1), time, scraped ETA from ShopeeFood/Grab (simulated), recent community reports, static menu tags.

Outputs
- Two recommended restaurants with: predicted ETA, confidence, short rationale, links to source entries.

Happy Path
- Predictions match real-world delivery and user orders successfully within predicted window.

Failure Path
- Predictions are incorrect; prototype shows fallback alternatives and records feedback for evidence owner.

Success Criteria (Day 06 prototype)
- Prototype returns 2 suggestions within 2s for given fake dataset.  
- For 5 test cases (fake/controlled), predicted ETA within ±15 minutes of ground truth for ≥4 cases.  
- UI shows sources and confidence visibly.  
- Demo script (3 minutes) runs end‑to‑end with fake data.

Scope Day 06
- Build a minimal web UI (static pages + minimal backend) that reads fake data from SQLite and runs a simple ranking heuristic.  
- No live scraping, no payment flow, no integration with real delivery APIs.

Out of Scope
- Real-time scraping pipeline, payment processing, full search across all cuisines, trust/verification system beyond simple source links.

## Risks (top 10) and mitigations
1. Evidence weak → Mitigation: focus on self‑use + 10 FB posts + 10 delivery reviews.  
2. Data mismatch in demo → Use controlled fake data and document assumptions.  
3. Overclaiming AI capability → Show confidence and sources.  
4. Privacy concerns from scraped posts → Use quotes anonymized and public posts only.  
5. Prototype can't demo latency → Precompute results; use SQLite queries.  
6. Team misaligned on scope → Daily timeline and owner sign‑off checkpoints.  
7. Failure path not tested → Assign owner to create 2 failure test cases.  
8. Demo owner unavailable → Prep recorded demo fallback.  
9. User payment assumption invalid → Mark monetization as hypothesis, require validation.  
10. Platform TOS issues for scraping → Use simulated data and public permalinks only.

---
End of description.md
