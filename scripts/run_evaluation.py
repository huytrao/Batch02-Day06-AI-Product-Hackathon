"""Run demo evaluation cases and automatically append results to artifacts.

By default this script calls POST /api/query on http://127.0.0.1:8000. If the
API is not running, it still writes a timestamped failure log so the team has
evidence of what was attempted.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
EVALUATION_LOG = ARTIFACTS_DIR / "evaluation_log.md"
EVIDENCE_LOG = ARTIFACTS_DIR / "evidence_log.md"


EVALUATION_CASES = [
    {
        "case_id": "EV-001",
        "name": "Happy path",
        "query": "Giao nhanh ở Ocean Park 1",
        "location": "Ocean Park 1",
        "expected": "Return at least one suggestion with action_trace and confidence.",
    },
    {
        "case_id": "EV-002",
        "name": "Low confidence",
        "query": "Tìm món rất hiếm gần Ocean Park 1",
        "location": "Ocean Park 1",
        "expected": "Return low-confidence result or ask clarification with evidence.",
    },
    {
        "case_id": "EV-003",
        "name": "Failure path",
        "query": "Tìm quán mở lúc 3 giờ sáng ở Ocean Park 1",
        "location": "Ocean Park 1",
        "expected": "Handle unavailable/closed case without fake certainty.",
    },
    {
        "case_id": "EV-004",
        "name": "Correction",
        "query": "Quán đầu tiên đang đóng, gợi ý quán khác",
        "location": "Ocean Park 1",
        "expected": "Adjust recommendation and record correction context.",
    },
    {
        "case_id": "EV-005",
        "name": "Feedback submit",
        "query": "Gợi ý đồ ăn trưa giao nhanh",
        "location": "Ocean Park 1",
        "expected": "Suggestion can be followed by feedback submission.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def post_json(url: str, payload: dict[str, str], timeout: float) -> tuple[int, dict | list | str]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
        try:
            parsed: dict | list | str = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
        return response.status, parsed


def evaluate_response(body: dict | list | str) -> tuple[bool, str, str, str]:
    if not isinstance(body, dict):
        return False, "non_json_response", "", ""

    suggestions = body.get("suggestions") or body.get("final_answer", {}).get("suggestions") or []
    trace = body.get("action_trace") or body.get("final_answer", {}).get("action_trace") or []
    confidence = ""
    if suggestions and isinstance(suggestions, list):
        first = suggestions[0]
        if isinstance(first, dict):
            confidence = str(first.get("confidence") or first.get("confidence_label") or "")

    passed = bool(suggestions or trace or body.get("clarification"))
    actual = "suggestions=%s; trace_steps=%s; clarification=%s" % (
        len(suggestions) if isinstance(suggestions, list) else 0,
        len(trace) if isinstance(trace, list) else 0,
        bool(body.get("clarification")),
    )
    note = "API returned usable demo structure." if passed else "Missing suggestions/action_trace/clarification."
    return passed, actual, confidence, note


def run_case(case: dict[str, str], endpoint: str, timeout: float) -> dict[str, object]:
    started = time.perf_counter()
    payload = {"query": case["query"], "location": case["location"]}
    try:
        status_code, body = post_json(endpoint, payload, timeout)
        latency_ms = int((time.perf_counter() - started) * 1000)
        passed, actual, confidence, note = evaluate_response(body)
        return {
            **case,
            "timestamp": utc_now(),
            "status_code": status_code,
            "latency_ms": latency_ms,
            "confidence": confidence,
            "actual": actual,
            "pass_fail": "PASS" if passed else "FAIL",
            "note": note,
            "response_preview": json.dumps(body, ensure_ascii=False)[:800],
        }
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return {
            **case,
            "timestamp": utc_now(),
            "status_code": None,
            "latency_ms": latency_ms,
            "confidence": "",
            "actual": "API unavailable or request failed.",
            "pass_fail": "FAIL",
            "note": f"{type(exc).__name__}: {exc}",
            "response_preview": "",
        }


def format_markdown_result(result: dict[str, object]) -> str:
    return (
        f"\n## {result['timestamp']} - {result['case_id']} - {result['name']}\n"
        f"- Query: {result['query']}\n"
        f"- Expected: {result['expected']}\n"
        f"- Actual: {result['actual']}\n"
        f"- Latency: {result['latency_ms']} ms\n"
        f"- Confidence: {result['confidence'] or 'n/a'}\n"
        f"- Pass/Fail: {result['pass_fail']}\n"
        f"- Note: {result['note']}\n"
        f"- Response preview: `{result['response_preview'] or 'n/a'}`\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run evaluation cases and append logs automatically.")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000/api/query")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    append_text(EVALUATION_LOG, f"\n# Evaluation Run - {utc_now()}\n")
    append_text(EVIDENCE_LOG, f"\n# Evidence Run - {utc_now()}\n")

    results = [run_case(case, args.endpoint, args.timeout) for case in EVALUATION_CASES]
    for result in results:
        append_text(EVALUATION_LOG, format_markdown_result(result))
        append_text(
            EVIDENCE_LOG,
            (
                f"\n## {result['timestamp']} - {result['case_id']}\n"
                f"- Evidence type: evaluation_api_call\n"
                f"- Owner: Member E - Trảo An Huy\n"
                f"- Endpoint: {args.endpoint}\n"
                f"- Status: {result['pass_fail']}\n"
                f"- Linked log: artifacts/evaluation_log.md\n"
            ),
        )

    passed = sum(1 for result in results if result["pass_fail"] == "PASS")
    print(f"Evaluation complete: {passed}/{len(results)} passed")
    print(f"Wrote: {EVALUATION_LOG}")
    print(f"Wrote: {EVIDENCE_LOG}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
