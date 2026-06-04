# Evaluation Plan

Owner: Member E - Trảo An Huy

## Metrics

- Pass/fail for each case.
- API latency in milliseconds.
- Confidence returned by the agent when available.
- Expected result vs actual result.
- Evidence link to generated logs.

## Test Cases

| Case | Path | Query | Expected |
| --- | --- | --- | --- |
| EV-001 | Happy path | Giao nhanh ở Ocean Park 1 | Returns at least one suggestion with action trace and confidence. |
| EV-002 | Low confidence | Tìm món rất hiếm gần Ocean Park 1 | Returns low-confidence result or asks clarification with evidence. |
| EV-003 | Failure path | Tìm quán mở lúc 3 giờ sáng ở Ocean Park 1 | Handles unavailable/closed case without fake certainty. |
| EV-004 | Correction | Quán đầu tiên đang đóng, gợi ý quán khác | Adjusts recommendation and records correction context. |
| EV-005 | Feedback submit | Gợi ý đồ ăn trưa giao nhanh | Suggestion can be followed by feedback submission. |

## How To Run

Start the API, then run:

```bash
python scripts/run_evaluation.py
python scripts/collect_evidence.py
```

The scripts append results automatically to `artifacts/evaluation_log.md` and `artifacts/evidence_log.md`.
