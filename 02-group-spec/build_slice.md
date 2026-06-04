Project: **Ocean Park 1 Eats — Aggregated Dining Info**  
Chosen Slice: **Slice B — Fast Delivery Suggestion**  
Owner: **CTh — Product Spec Owner**  
Version: **Day 05 final-ready spec**

---

## 0. Spec Summary

This file defines the build slice for Day 06 prototype. The goal is not to build a full food discovery app. The goal is to prove one narrow product decision:

> **Can we help a busy Ocean Park 1 resident choose 2 food options that are likely to arrive within 30–45 minutes, while showing confidence, evidence, and fallback actions when the data is uncertain?**

The final slice is intentionally narrow:

- **One user:** Busy Ocean Park 1 resident.
- **One task:** Choose where to order food when they need fast delivery.
- **One AI decision:** Rank restaurants by predicted delivery speed and confidence.
- **One output:** 2 recommended restaurants with ETA, confidence, reason, sources, and fallback.
- **Human control:** AI does **not** place the order. User always confirms in the delivery app or by calling the vendor.

---

## 1. Product Context

### Problem

Residents of Ocean Park 1 struggle to make quick meal decisions because food information is scattered across:

- Facebook resident groups.
- Google Maps opening hours and reviews.
- ShopeeFood / GrabFood ETA and menu pages.
- Informal community reports.

This creates 3 repeated user problems:

1. **Search cost:** User must open many platforms before deciding.
2. **Trust gap:** App ETA, opening status, and community comments may conflict.
3. **Failed order risk:** User may pick a restaurant that looks fast but is closed, overloaded, or slow to deliver.

### Opportunity

For Ocean Park 1 residents who need a quick meal decision, the product should aggregate local signals and return a small, explainable recommendation set.

The product should not pretend to know everything. It should show:

- What it recommends.
- Why it recommends it.
- How confident it is.
- Which source signals support the recommendation.
- What the user should do when confidence is low.

---

## 2. Evidence Contract

This spec does not invent evidence. It defines how evidence will be used by the prototype.

### Evidence needed from Research / Evidence owners

| Evidence ID | Needed evidence | Why it matters | Required minimum for Day 06 |
|---|---|---|---|
| E1 | Self-use notes from trying to order food in Ocean Park 1 | Proves the pain exists from real workflow | At least 3 timestamped attempts |
| E2 | Facebook posts/comments about “ăn gì”, “giao nhanh”, “ship chậm”, “quán đóng cửa” | Captures local real-time community signals | At least 10 relevant posts/comments |
| E3 | Google Maps opening-hour or recent review snippets | Helps validate open/closed and reliability | At least 5 restaurants |
| E4 | ShopeeFood / GrabFood ETA screenshots or manual records | Main input for delivery ETA prediction | At least 10 restaurant-platform rows |
| E5 | Negative cases: delayed delivery, closed shop, unavailable menu | Needed to test failure path | At least 3 failure examples |
| E6 | User correction examples or assumed correction scenarios | Needed to test correction path | At least 2 correction scenarios |

### Evidence rule

A recommendation is allowed to show **HIGH confidence** only if it has at least:

- 2 recent ETA signals from platform or controlled sample data, and
- no fresh negative report within the last 30 minutes, and
- no open/closed conflict.

If those conditions are not met, the UI must show **MEDIUM** or **LOW** confidence.

---

## 3. Three Candidate Build Slices

### Slice A — Quick Open + Cuisine Finder

| Field | Spec |
|---|---|
| Target user | Resident who wants to know which nearby restaurants are open in the next 30 minutes. |
| Core task | Find currently open restaurants by cuisine. |
| AI decision | Infer “open now” confidence from Google Maps hours, recent posts, and user reports. |
| Output | Top 3 restaurants that are likely open, with cuisine tag, confidence, and source links. |
| Human control | User decides whether to visit, call, or order. |
| Main failure risk | AI marks a restaurant open when it is actually closed. |
| Mitigation | Show source timestamp, phone/call button, and warning if data is stale. |
| Feasibility for 6h prototype | Medium. Opening-hour data can be simulated, but real open/closed verification is risky. |

### Slice B — Fast Delivery Suggestion — **Chosen**

| Field | Spec |
|---|---|
| Target user | Busy Ocean Park 1 resident who wants food delivered within 30–45 minutes. |
| Core task | Choose 1 of 2 fast delivery options without checking many apps manually. |
| AI decision | Predict expected delivery time and confidence using ETA signals, recent reports, open status, distance, and preparation-speed tags. |
| Output | 2 restaurant recommendations with predicted ETA, confidence, short reason, source links, and fallback action. |
| Human control | User reviews evidence and confirms order in delivery app or by calling. AI never places the order. |
| Main failure risk | AI recommends “fast delivery” but actual order is delayed, canceled, closed, or unavailable. |
| Mitigation | Show confidence, source timestamps, fallback pickup/call options, and correction/report flow. |
| Feasibility for 6h prototype | High. Can be built with SQLite + fake controlled ETA data + simple ranking heuristic. |

### Slice C — Dietary Filtered Suggestion

| Field | Spec |
|---|---|
| Target user | Resident or visitor who needs vegetarian or halal-friendly food. |
| Core task | Find restaurants matching a dietary constraint. |
| AI decision | Classify restaurant/menu evidence into dietary tags and confidence levels. |
| Output | Top 3 restaurants with dietary tag, confidence, and source quotes. |
| Human control | User checks source evidence before ordering. |
| Main failure risk | AI incorrectly labels a restaurant vegetarian/halal-friendly, causing user harm or serious distrust. |
| Mitigation | Require direct source quote, show uncertainty, allow correction, avoid unsupported claims. |
| Feasibility for 6h prototype | Medium-low. Dietary claims require stronger verification and are riskier than speed ranking. |

---

## 4. Final Slice Selection

### Chosen slice

**Slice B — Fast Delivery Suggestion**

### Why this slice wins

| Criterion | Slice A: Open + Cuisine | Slice B: Fast Delivery | Slice C: Dietary Filter |
|---|---:|---:|---:|
| User pain frequency | High | High | Medium |
| Demo clarity in 3 minutes | Medium | High | Medium |
| Data availability for fake prototype | Medium | High | Medium |
| Easy to test with controlled cases | Medium | High | Medium |
| Risk of harmful wrong output | Medium | Medium | High |
| Narrowness of task | Medium | High | Medium |
| Fits Day 06 6h build | Medium | High | Medium-low |

### Decision rationale

Slice B is selected because it has the strongest combination of:

1. **Narrow task:** “I need food quickly” is more precise than general food discovery.
2. **Clear AI decision:** predict and rank delivery ETA.
3. **Testable output:** predicted ETA can be compared against controlled ground truth in fake data.
4. **Demo value:** user flow is short: choose “Giao nhanh” → see 2 options → inspect confidence → confirm order.
5. **Moderate risk, manageable fallback:** late delivery is frustrating but can be mitigated through confidence labels and fallback options.

### Why not Slice A

Slice A is useful, but “open now” can be misleading without real-time vendor confirmation. A restaurant may appear open on Google Maps but stop accepting delivery orders. This makes the failure mode harder to prove in a fake prototype.

### Why not Slice C

Slice C has higher sensitivity. Vegetarian/halal labels should not be inferred loosely because a wrong label can violate user dietary requirements. It needs stronger evidence, direct menu verification, and more careful source quoting than a 6-hour prototype can support.

---

## 5. Final Build Slice Definition

### User story

> As a busy Ocean Park 1 resident, I want to see 2 food options that are likely to arrive within 30–45 minutes, so that I can order quickly without opening Facebook, Google Maps, ShopeeFood, and GrabFood one by one.

### Job to be done

When I am hungry and short on time, help me choose a nearby restaurant that can deliver fast **now**, while warning me if the evidence is weak or conflicting.

### In scope

- Ocean Park 1 only.
- Fast delivery use case only.
- 2 recommended restaurants only.
- Fake/controlled data in SQLite or CSV.
- Simple ranking heuristic that simulates AI decision-making.
- Source links or source labels are displayed.
- Confidence labels are displayed.
- User correction is supported.

### Out of scope

- No live scraping.
- No payment.
- No automatic order placement.
- No full restaurant search engine.
- No real integration with ShopeeFood / GrabFood APIs.
- No claim that ETA is guaranteed.
- No hidden automation that affects user money or food order.

---

## 6. Auto / Aug Decision

### Final decision

**Augmentation-first, not full automation.**

The AI ranks options and explains why. The human makes the ordering decision.

### Roles

| Actor | Responsibility |
|---|---|
| AI | Calculate predicted ETA, confidence, ranking, and explanation. |
| User | Decide whether to order, call, pick up, or ignore the recommendation. |
| System | Display source evidence, confidence, fallback options, and correction form. |
| Evidence Owner | Review flagged corrections and update trusted data. |

### What AI is allowed to do

AI can:

- Rank restaurants.
- Predict ETA range.
- Assign confidence level.
- Explain source conflict.
- Suggest fallback actions.
- Temporarily lower ranking after user correction.

### What AI is not allowed to do

AI cannot:

- Place an order automatically.
- Pay automatically.
- Hide source uncertainty.
- Claim guaranteed delivery.
- Mark dietary or open/closed status as certain without evidence.
- Permanently change database truth based on one unverified report.

### Limited conditional automation

The only conditional automation allowed is low-risk:

- If a user submits a correction, the system may temporarily flag the restaurant as “needs verification”.
- If 2 or more recent negative reports appear within 30 minutes, the system may lower confidence automatically.
- Permanent database update requires Evidence Owner review.

---

## 7. AI Decision Specification

### Decision question

For each restaurant candidate:

> “Given the current time, app ETA signals, community reports, open status, distance, and preparation-speed tag, how likely is this restaurant to deliver within 45 minutes?”

### Required input fields

| Field | Type | Example | Purpose |
|---|---|---|---|
| restaurant_id | string | `r_001` | Unique restaurant key |
| restaurant_name | string | `Bánh Mì A` | Display name |
| cuisine_tag | string | `banh_mi` | Helps user understand option |
| location_zone | string | `S1`, `S2`, `Masteri`, `OP1` | Helps estimate distance |
| distance_minutes_walk | integer | `8` | Fallback pickup estimate |
| is_listed_open | boolean | `true` | Basic eligibility check |
| last_open_source_time | datetime | `2026-06-03 11:40` | Freshness check |
| grab_eta_min | integer/null | `25` | Platform signal |
| shopee_eta_min | integer/null | `35` | Platform signal |
| platform_eta_timestamp | datetime | `2026-06-03 11:45` | ETA freshness |
| recent_report_eta_min | integer/null | `40` | Community signal |
| recent_report_sentiment | enum | `positive`, `neutral`, `negative` | Delay signal |
| recent_report_time | datetime/null | `2026-06-03 11:35` | Freshness of report |
| prep_speed_tag | enum | `fast`, `medium`, `slow` | Preparation estimate |
| negative_report_count_30m | integer | `0`, `1`, `2` | Conflict/risk signal |
| evidence_links | list | `[grab_screen_01, fb_post_03]` | Explainability |

### Output fields

| Field | Type | Example |
|---|---|---|
| restaurant_name | string | `Bánh Mì A` |
| predicted_eta_range | string | `30–40 min` |
| confidence | enum | `HIGH`, `MEDIUM`, `LOW` |
| recommendation_rank | integer | `1` |
| reason | string | `Grab 25m, Shopee 35m, no negative reports in 30m.` |
| source_summary | string | `2 app ETA signals + 1 recent community report.` |
| fallback_action | string | `Order in app`, `Call first`, `Pickup suggested` |
| warning | string/null | `ETA signals conflict; check before ordering.` |

---

## 8. Ranking and Confidence Rules

The prototype does not need a complex ML model. For Day 06, use a transparent heuristic so the team can demo, test, and debug it.

### 8.1 Candidate eligibility

A restaurant is eligible only if:

```text
is_listed_open = true
AND at least one ETA signal exists
AND platform_eta_timestamp is not older than 60 minutes
```

If `is_listed_open = false`, the restaurant must not be shown as a normal recommendation. It may appear only as a low-confidence item with “Call first” if the user explicitly asks to inspect it.

### 8.2 Predicted ETA

Use the median of available ETA signals, then apply penalties.

```text
base_eta = median(grab_eta_min, shopee_eta_min, recent_report_eta_min)

prep_penalty:
- fast = +0
- medium = +5
- slow = +10

negative_report_penalty:
- 0 negative reports in last 30m = +0
- 1 negative report in last 30m = +10
- 2 or more negative reports in last 30m = +20

open_uncertainty_penalty:
- last open-source update <= 60m = +0
- 61–180m = +10
- >180m or unknown = +20

predicted_eta = base_eta + prep_penalty + negative_report_penalty + open_uncertainty_penalty
```

### 8.3 ETA display range

```text
If confidence = HIGH: display predicted_eta ± 5 minutes
If confidence = MEDIUM: display predicted_eta ± 10 minutes
If confidence = LOW: display predicted_eta ± 15 minutes and warning
```

Examples:

- Predicted 35, HIGH → `30–40 min`
- Predicted 45, MEDIUM → `35–55 min`
- Predicted 55, LOW → `40–70 min, check before ordering`

### 8.4 Confidence rules

| Confidence | Rule |
|---|---|
| HIGH | At least 2 fresh ETA signals, ETA spread <= 10 minutes, no negative report in last 30 minutes, open status fresh <= 60 minutes. |
| MEDIUM | At least 1 fresh ETA signal, ETA spread <= 20 minutes, no more than 1 negative report in last 30 minutes. |
| LOW | ETA spread > 20 minutes, or 2+ negative reports, or open status stale/unknown, or source conflict exists. |

### 8.5 Ranking score

Lower score is better.

```text
ranking_score = predicted_eta
              + confidence_penalty
              + distance_penalty

confidence_penalty:
- HIGH = +0
- MEDIUM = +8
- LOW = +20

distance_penalty:
- distance_minutes_walk <= 5 = +0
- 6–10 = +3
- >10 = +6
```

Return the 2 restaurants with the lowest ranking score.

### 8.6 Do not over-rank low confidence

A LOW confidence option cannot appear as rank #1 unless all available candidates are LOW confidence. If all candidates are LOW confidence, the UI must switch from “Recommended” to “Check before ordering”.

---

## 9. UI Output Contract

Each recommendation card must show:

```text
Restaurant name
Cuisine tag
Predicted ETA range
Confidence badge
Reason in 1 sentence
Source summary
Primary action
Fallback action
Correction button
```

### Example card — HIGH confidence

```text
Bánh Mì A
Fast snack · OP1 S1
ETA: 30–40 min
Confidence: HIGH
Reason: Grab 25m and Shopee 35m are consistent; no delay reports in last 30m.
Sources: Grab ETA screenshot, ShopeeFood ETA record, 1 recent resident report.
Action: Open delivery app
Fallback: Call vendor
Report: Wrong info?
```

### Example card — LOW confidence

```text
Phở B
Noodle · OP1 S2
ETA: 45–70 min
Confidence: LOW
Warning: ETA signals conflict. Grab shows 25m, but 2 resident reports mention delivery delay in the last 20m.
Sources: Grab ETA screenshot, Facebook resident reports.
Action: Check app before ordering
Fallback: Choose pickup / Call vendor
Report: Wrong info?
```

---

## 10. Detailed Four Paths

### 10.1 Happy Path

| Item | Detail |
|---|---|
| User context | User is hungry and wants food delivered within 45 minutes. |
| Input | Current time: 12:10. User selects “Giao nhanh”. Location: Ocean Park 1. |
| Data state | Grab ETA and ShopeeFood ETA are fresh and consistent. No negative reports. Restaurant is listed open. |
| AI decision | Predict ETA 35 minutes, confidence HIGH. |
| UI output | Show 2 restaurants with ETA 30–40 min and HIGH confidence. |
| User action | User opens delivery app and orders. |
| Success condition | User can decide within 30 seconds and sees why options were recommended. |

#### Happy Path test case

```yaml
test_id: HP-01
restaurant: Banh Mi A
grab_eta_min: 30
shopee_eta_min: 35
recent_report_eta_min: 35
negative_report_count_30m: 0
is_listed_open: true
last_open_source_age_min: 20
prep_speed_tag: fast
expected_confidence: HIGH
expected_eta_range: 30-40
expected_ui_warning: null
expected_primary_action: Open delivery app
```

---

### 10.2 Low Confidence Path

| Item | Detail |
|---|---|
| User context | User wants fast delivery during rain or peak hour. |
| Input | User selects “Giao nhanh”. |
| Data state | App ETA says 25 minutes, but recent community reports say delivery is slow. ETA signals conflict. |
| AI decision | Do not hide the restaurant, but lower confidence to LOW and widen ETA range. |
| UI output | Show warning: “ETA signals conflict. Check before ordering.” |
| User action | User may call vendor, choose pickup, or pick another restaurant. |
| Success condition | User understands uncertainty before placing an order. |

#### Low Confidence test case

```yaml
test_id: LC-01
restaurant: Pho B
grab_eta_min: 25
shopee_eta_min: 55
recent_report_eta_min: 60
negative_report_count_30m: 2
is_listed_open: true
last_open_source_age_min: 50
prep_speed_tag: medium
expected_confidence: LOW
expected_eta_range: 45-75
expected_ui_warning: ETA signals conflict; check before ordering.
expected_primary_action: Check app before ordering
expected_fallback_action: Call vendor or choose pickup
```

---

### 10.3 Failure Path

| Item | Detail |
|---|---|
| User context | User follows a HIGH confidence recommendation. |
| Failure | Restaurant is actually closed, unavailable, or order becomes delayed >60 minutes. |
| Cause | Data was stale or platform did not update availability. |
| AI/system response | Apologize, show alternatives, ask user to report what happened. |
| UI output | “This recommendation may be wrong. Here are 2 safer nearby options.” |
| Data action | Log mismatch and flag restaurant as needs verification. |
| Success condition | Failure is recoverable and improves future data quality. |

#### Failure Path test case

```yaml
test_id: FP-01
restaurant: Rice C
grab_eta_min: 30
shopee_eta_min: 35
recent_report_eta_min: null
negative_report_count_30m: 0
is_listed_open: true
last_open_source_age_min: 240
prep_speed_tag: fast
actual_outcome: restaurant_closed
expected_confidence: LOW
expected_reason: Open status is stale over 180 minutes.
expected_ui_warning: Call first; opening data may be outdated.
expected_recovery: Show 2 alternative restaurants and report button.
```

### Failure mode severity

| Failure | Severity | Why |
|---|---|---|
| ETA off by 10 minutes | Low | User still receives food close to expectation. |
| ETA off by 20–30 minutes | Medium | User loses time and trust. |
| Restaurant closed / no delivery | High | User cannot complete task and must restart. |
| AI orders automatically | Unacceptable | Outside scope and violates human control. |

### Worst failure

The worst realistic failure for this slice is:

> AI recommends a restaurant as fast and available, but the restaurant is closed or cannot deliver, causing the user to waste time and possibly lose trust in the product.

### Prototype handling

The prototype must handle this by:

1. Never showing unsupported certainty.
2. Showing source timestamps.
3. Using LOW confidence if open status is stale.
4. Providing fallback actions: call, pickup, choose another restaurant.
5. Logging correction for Evidence Owner review.

---

### 10.4 Correction Path

| Item | Detail |
|---|---|
| User context | User notices the recommendation contains wrong information. |
| Correction examples | Closed restaurant, wrong ETA, wrong location, wrong phone number, unavailable menu. |
| User action | User taps “Report wrong info”. |
| System response | Show short correction form. |
| AI/system decision | Temporarily lower confidence or hide the item from top recommendations if correction is serious. |
| Human review | Evidence Owner verifies before permanent update. |
| Success condition | User can correct the system in under 20 seconds. |

#### Correction form fields

```text
What is wrong?
[ ] Restaurant closed
[ ] Delivery unavailable
[ ] ETA was much slower
[ ] Wrong location
[ ] Wrong phone number
[ ] Menu unavailable
[ ] Other

Optional note:
[free text]

Optional source:
[photo/link/screenshot]
```

#### Correction Path test case

```yaml
test_id: CP-01
restaurant: Chicken D
user_report_type: Restaurant closed
report_time: 2026-06-03 12:20
previous_confidence: HIGH
expected_immediate_action: Lower restaurant confidence to LOW for current session.
expected_database_action: Create verification ticket for Evidence Owner.
expected_ui_message: Thanks. We flagged this place for review and will avoid recommending it as high confidence.
```

---

## 11. Prototype Data Model

### Table: restaurants

```sql
CREATE TABLE restaurants (
  restaurant_id TEXT PRIMARY KEY,
  restaurant_name TEXT NOT NULL,
  cuisine_tag TEXT,
  location_zone TEXT,
  distance_minutes_walk INTEGER,
  is_listed_open BOOLEAN,
  last_open_source_time TEXT,
  phone_number TEXT,
  delivery_app_link TEXT
);
```

### Table: eta_signals

```sql
CREATE TABLE eta_signals (
  signal_id TEXT PRIMARY KEY,
  restaurant_id TEXT,
  source_type TEXT, -- grab, shopeefood, community_report, google_maps
  eta_min INTEGER,
  sentiment TEXT, -- positive, neutral, negative
  source_time TEXT,
  source_label TEXT,
  source_link TEXT,
  FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);
```

### Table: recommendation_logs

```sql
CREATE TABLE recommendation_logs (
  log_id TEXT PRIMARY KEY,
  created_at TEXT,
  user_location_zone TEXT,
  restaurant_id TEXT,
  predicted_eta_min INTEGER,
  confidence TEXT,
  ranking_score REAL,
  shown_to_user BOOLEAN,
  user_action TEXT,
  FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);
```

### Table: correction_reports

```sql
CREATE TABLE correction_reports (
  report_id TEXT PRIMARY KEY,
  created_at TEXT,
  restaurant_id TEXT,
  report_type TEXT,
  user_note TEXT,
  evidence_link TEXT,
  review_status TEXT, -- pending, accepted, rejected
  FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);
```

---

## 12. Sample Controlled Data

```csv
restaurant_id,restaurant_name,cuisine_tag,location_zone,distance_minutes_walk,is_listed_open,last_open_source_age_min,grab_eta_min,shopee_eta_min,recent_report_eta_min,negative_report_count_30m,prep_speed_tag,expected_confidence
r_001,Banh Mi A,banh_mi,S1,5,true,20,30,35,35,0,fast,HIGH
r_002,Pho B,pho,S2,8,true,50,25,55,60,2,medium,LOW
r_003,Rice C,rice,S1,4,true,240,30,35,,0,fast,LOW
r_004,Chicken D,chicken,S3,12,true,40,40,45,45,0,medium,MEDIUM
r_005,Noodles E,noodle,S2,7,false,10,20,25,25,0,fast,EXCLUDE
```

---

## 13. Acceptance Criteria

The Day 06 prototype is acceptable only if all criteria below are met.

### Functional criteria

- User can select “Giao nhanh”.
- System returns exactly 2 recommendation cards.
- Each card shows ETA range, confidence, reason, and source summary.
- LOW confidence cases show a visible warning.
- User can open fallback action: call, pickup, or choose alternative.
- User can submit a correction.

### AI decision criteria

- Ranking uses explicit ETA/confidence rules, not random ordering.
- HIGH confidence is only shown when source rules are satisfied.
- LOW confidence is shown when ETA signals conflict or open status is stale.
- No automatic order placement exists.

### Testing criteria

- At least 5 controlled test cases exist.
- At least 1 happy path test exists.
- At least 1 low-confidence test exists.
- At least 1 failure test exists.
- At least 1 correction test exists.
- For controlled test cases, predicted ETA must be within ±15 minutes of expected ground truth in at least 4/5 cases.

### UX criteria

- User can understand the recommendation in under 10 seconds.
- The reason is one sentence, not a long paragraph.
- Confidence badge is visually obvious.
- Source timestamp is visible or available on click.
- Fallback is shown when confidence is MEDIUM or LOW.

---

## 14. Handoff Notes for Prototype Owner

### Minimal screen flow

```text
Screen 1: Home
- Button: “Giao nhanh trong 45 phút”
- Optional: location zone selector

Screen 2: Recommendation results
- Card 1: best option
- Card 2: second best option
- Confidence + ETA + reason + source summary
- CTA: Open delivery app / Call vendor
- CTA: Report wrong info

Screen 3: Correction form
- Select issue type
- Optional note
- Submit

Screen 4: Recovery / fallback
- If LOW confidence or failure: show safer alternatives / pickup options
```

### Required backend function

```python
def recommend_fast_delivery(user_zone: str, current_time: datetime) -> list[Recommendation]:
    """
    Return top 2 restaurant recommendations with:
    - predicted ETA range
    - confidence
    - reason
    - source summary
    - fallback action
    """
```

### Required helper functions

```python
calculate_predicted_eta(candidate)
calculate_confidence(candidate)
calculate_ranking_score(candidate)
build_explanation(candidate)
handle_correction(report)
```

---

## 15. Handoff Notes for Evidence Owner

Evidence Owner should validate whether the prototype assumptions match real user evidence.

### Evidence validation checklist

- Are “fast delivery” complaints actually present in the collected data?
- Do users mention opening multiple apps before deciding?
- Are Facebook/community reports useful for delay detection?
- Are platform ETAs inconsistent often enough to justify aggregation?
- Are closed/unavailable restaurants a repeated failure mode?

### Source labeling rule

Each source must be labeled by type:

```text
APP_ETA_GRAB
APP_ETA_SHOPEE
GOOGLE_MAPS_HOURS
FB_COMMUNITY_REPORT
SELF_USE_LOG
USER_CORRECTION
```

### Evidence freshness rule

| Source type | Freshness requirement |
|---|---|
| App ETA | <= 60 minutes |
| Community delay report | <= 30 minutes for confidence impact |
| Google Maps opening hours | <= 7 days for static display, <= 60 minutes for HIGH confidence open-now claim |
| Self-use log | Same day preferred |
| User correction | Immediate flag, human review later |

---

## 16. Demo Script Alignment

The 3-minute demo should show exactly 3 moments:

### Moment 1 — Happy path

User clicks “Giao nhanh trong 45 phút”. System shows 2 options with HIGH/MEDIUM confidence.

### Moment 2 — Low confidence path

System shows a conflicting ETA case and warns the user instead of overclaiming.

### Moment 3 — Correction / failure recovery

User reports “restaurant closed”. System lowers confidence and shows alternative options.

This proves the product is not just a recommendation list. It proves the system can handle uncertainty.

---

## 17. Product Guardrails

### Do not say

- “Guaranteed delivery in 30 minutes.”
- “This restaurant is definitely open.”
- “AI found the best restaurant.”
- “Order automatically.”

### Say instead

- “Likely 30–40 minutes based on recent signals.”
- “Confidence: HIGH / MEDIUM / LOW.”
- “Check before ordering when confidence is low.”
- “AI suggests; user decides.”

---

## 18. Final Position

The final build slice is:

> **Fast Delivery Suggestion for Ocean Park 1 residents: AI ranks 2 likely-fast delivery options using ETA signals, community reports, open-status freshness, and prep-speed tags. The system shows ETA range, confidence, reason, sources, and fallback actions. AI suggests; user decides.**

This slice is strong because it is narrow, buildable, testable, honest about uncertainty, and aligned with the Day 06 prototype constraints.
