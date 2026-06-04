from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
TEST_LOG_DIR = PROJECT_ROOT / "test_logs"
PYTEST_CONFIG = None

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _now_for_filename():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def pytest_configure(config):
    global PYTEST_CONFIG
    PYTEST_CONFIG = config
    TEST_LOG_DIR.mkdir(exist_ok=True)
    config.react_agent_cases = []
    config.react_agent_report_path = (
        TEST_LOG_DIR / f"react_agent_report_{_now_for_filename()}.md"
    )
    config.react_agent_outcomes = {"passed": 0, "failed": 0, "skipped": 0}


def pytest_runtest_logreport(report):
    if report.when != "call":
        return

    config = PYTEST_CONFIG
    if config is None:
        return

    if report.passed:
        config.react_agent_outcomes["passed"] += 1
    elif report.failed:
        config.react_agent_outcomes["failed"] += 1
    elif report.skipped:
        config.react_agent_outcomes["skipped"] += 1


def record_agent_case(
    config,
    *,
    case_id,
    user_query,
    result,
    provider,
    expected_tools,
    quality_score,
    quality_notes,
):
    actual_tools = [
        step["tool"]
        for step in result.get("action_trace", [])
        if step.get("type") == "action"
    ]
    system_prompt = getattr(provider, "system_prompt_seen", "") or ""

    config.react_agent_cases.append(
        {
            "case_id": case_id,
            "user_query": user_query,
            "status": "fail" if "error" in result else "pass",
            "expected_tools": expected_tools,
            "actual_tools": actual_tools,
            "tool_count": len(actual_tools),
            "system_prompt_chars": len(system_prompt),
            "system_prompt_sha256": hashlib.sha256(
                system_prompt.encode("utf-8")
            ).hexdigest()[:12],
            "system_prompt_preview": system_prompt[:300].replace("\n", " "),
            "quality_score": quality_score,
            "quality_notes": quality_notes,
            "final_answer": result.get("final_answer"),
            "error": result.get("error"),
        }
    )


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    outcomes = getattr(
        config, "react_agent_outcomes", {"passed": 0, "failed": 0, "skipped": 0}
    )
    report_path = config.react_agent_report_path
    cases = getattr(config, "react_agent_cases", [])

    lines = [
        "# ReAct Agent Test Report",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"Total pytest cases: {sum(outcomes.values())}",
        f"Passed: {outcomes['passed']}",
        f"Failed: {outcomes['failed']}",
        f"Skipped: {outcomes['skipped']}",
        f"Recorded agent scenarios: {len(cases)}",
        "",
        "## Scenario Summary",
        "",
    ]

    for case in cases:
        lines.extend(
            [
                f"### {case['case_id']}",
                "",
                f"- Query: {case['user_query']}",
                f"- Status: {case['status']}",
                f"- Expected tools: {', '.join(case['expected_tools']) or 'None'}",
                f"- Actual tools: {', '.join(case['actual_tools']) or 'None'}",
                f"- Tool count: {case['tool_count']}",
                f"- System prompt chars: {case['system_prompt_chars']}",
                f"- System prompt hash: {case['system_prompt_sha256']}",
                f"- System prompt preview: {case['system_prompt_preview']}",
                f"- Output quality score: {case['quality_score']}/100",
                f"- Output quality notes: {case['quality_notes']}",
                "",
                "Final answer:",
                "",
                "```json",
                json.dumps(case["final_answer"], ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        )
        if case["error"]:
            lines.extend(["Error:", "", f"```text\n{case['error']}\n```", ""])

    report_path.write_text("\n".join(lines), encoding="utf-8")

    terminalreporter.write_sep("=", "ReAct Agent Test Logs")
    terminalreporter.write_line(f"Logs saved to: {report_path}")
    terminalreporter.write_line(
        f"Pass/Fail summary: {outcomes['passed']} passed, "
        f"{outcomes['failed']} failed, {outcomes['skipped']} skipped"
    )
