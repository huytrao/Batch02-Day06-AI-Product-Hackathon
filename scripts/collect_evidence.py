"""Collect demo evidence automatically into artifacts/evidence_log.md."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
EVIDENCE_LOG = ARTIFACTS_DIR / "evidence_log.md"
REQUEST_LOG = ARTIFACTS_DIR / "request_response_log.jsonl"
EVALUATION_LOG = ARTIFACTS_DIR / "evaluation_log.md"
DEPLOY_LOG = ARTIFACTS_DIR / "deploy_log.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def tail_lines(path: Path, limit: int = 5) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-limit:]


def append_evidence(entry: str) -> None:
    EVIDENCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with EVIDENCE_LOG.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append automatic evidence summary.")
    parser.add_argument("--deploy-url", default="", help="Cloudflare Pages URL if available")
    parser.add_argument("--screenshot", action="append", default=[], help="Screenshot path to record")
    parser.add_argument("--owner", default="Member E - Trảo An Huy")
    args = parser.parse_args()

    request_tail = tail_lines(REQUEST_LOG)
    evaluation_exists = EVALUATION_LOG.exists()
    deploy_exists = DEPLOY_LOG.exists()

    entry = [
        f"\n# Evidence Collection - {utc_now()}\n",
        f"- Owner: {args.owner}\n",
        f"- Deploy URL: {args.deploy_url or 'n/a'}\n",
        f"- Evaluation log: {'present' if evaluation_exists else 'missing'} ({EVALUATION_LOG})\n",
        f"- Deploy log: {'present' if deploy_exists else 'missing'} ({DEPLOY_LOG})\n",
        f"- Request/response log: {'present' if REQUEST_LOG.exists() else 'missing'} ({REQUEST_LOG})\n",
    ]

    if args.screenshot:
        entry.append("- Screenshots:\n")
        for screenshot in args.screenshot:
            entry.append(f"  - {screenshot}\n")

    if request_tail:
        entry.append("- Latest API evidence:\n")
        for raw_line in request_tail:
            try:
                item = json.loads(raw_line)
                entry.append(
                    "  - {timestamp} {method} {path} status={status_code} latency={duration_ms}ms\n".format(
                        **item
                    )
                )
            except (json.JSONDecodeError, KeyError):
                entry.append(f"  - {raw_line[:160]}\n")

    append_evidence("".join(entry))
    print(f"Evidence collected: {EVIDENCE_LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
