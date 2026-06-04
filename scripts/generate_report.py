"""Generate the weekly feedback analytics report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "api"))

from analytics import write_weekly_report  # noqa: E402
from feedback_db import DEFAULT_DB_PATH, init_feedback_db  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate weekly feedback analytics JSON.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Path to feedback.sqlite")
    parser.add_argument("--days", type=int, default=7, help="Lookback period in days")
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "artifacts" / "weekly_feedback_report.json"),
        help="Output JSON path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    init_feedback_db(args.db)
    output_path = write_weekly_report(args.out, db_path=args.db, days=args.days)
    print(f"Generated report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
