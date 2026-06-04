# Evaluation Log

This file is appended automatically by `python scripts/run_evaluation.py`.

# Evaluation Run - 2026-06-04T04:14:03+00:00

## 2026-06-04T04:14:05+00:00 - EV-001 - Happy path
- Query: Giao nhanh ở Ocean Park 1
- Expected: Return at least one suggestion with action_trace and confidence.
- Actual: API unavailable or request failed.
- Latency: 2055 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:14:07+00:00 - EV-002 - Low confidence
- Query: Tìm món rất hiếm gần Ocean Park 1
- Expected: Return low-confidence result or ask clarification with evidence.
- Actual: API unavailable or request failed.
- Latency: 2040 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:14:09+00:00 - EV-003 - Failure path
- Query: Tìm quán mở lúc 3 giờ sáng ở Ocean Park 1
- Expected: Handle unavailable/closed case without fake certainty.
- Actual: API unavailable or request failed.
- Latency: 2044 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:14:11+00:00 - EV-004 - Correction
- Query: Quán đầu tiên đang đóng, gợi ý quán khác
- Expected: Adjust recommendation and record correction context.
- Actual: API unavailable or request failed.
- Latency: 2057 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:14:13+00:00 - EV-005 - Feedback submit
- Query: Gợi ý đồ ăn trưa giao nhanh
- Expected: Suggestion can be followed by feedback submission.
- Actual: API unavailable or request failed.
- Latency: 2054 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

# Evaluation Run - 2026-06-04T04:46:18+00:00

## 2026-06-04T04:46:20+00:00 - EV-001 - Happy path
- Query: Giao nhanh ở Ocean Park 1
- Expected: Return at least one suggestion with action_trace and confidence.
- Actual: API unavailable or request failed.
- Latency: 2035 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:46:22+00:00 - EV-002 - Low confidence
- Query: Tìm món rất hiếm gần Ocean Park 1
- Expected: Return low-confidence result or ask clarification with evidence.
- Actual: API unavailable or request failed.
- Latency: 2023 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:46:24+00:00 - EV-003 - Failure path
- Query: Tìm quán mở lúc 3 giờ sáng ở Ocean Park 1
- Expected: Handle unavailable/closed case without fake certainty.
- Actual: API unavailable or request failed.
- Latency: 2007 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:46:26+00:00 - EV-004 - Correction
- Query: Quán đầu tiên đang đóng, gợi ý quán khác
- Expected: Adjust recommendation and record correction context.
- Actual: API unavailable or request failed.
- Latency: 2022 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`

## 2026-06-04T04:46:28+00:00 - EV-005 - Feedback submit
- Query: Gợi ý đồ ăn trưa giao nhanh
- Expected: Suggestion can be followed by feedback submission.
- Actual: API unavailable or request failed.
- Latency: 2028 ms
- Confidence: n/a
- Pass/Fail: FAIL
- Note: URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- Response preview: `n/a`
