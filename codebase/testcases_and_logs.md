# Testcases and Logs

## Command

```bash
python -m pytest -q
```

## Generated logs

Pytest writes a Markdown report after each run:

```text
test_logs/react_agent_report_<timestamp>.md
```

The terminal also prints:

```text
Logs saved to: <path>
Pass/Fail summary: <passed> passed, <failed> failed, <skipped> skipped
```

## Current testcase coverage

### Fast delivery ReAct flow

Query:

```text
Giao nhanh ở Ocean Park 1
```

Expected:

- Agent calls `query_restaurants` with `location = Ocean Park 1`.
- Agent calls `get_eta_estimate` for a candidate.
- `action_trace` contains at least two actions.
- Final answer includes suggestion id, name, ETA, confidence, and reason.
- Runtime is under 2 seconds with the sample SQLite DB.

### Clarification flow

Query:

```text
Gợi ý quán sushi giao nhanh
```

Expected:

- Agent does not guess location.
- Agent calls `clarify`.
- Final answer asks for the missing location.

### Tool runner integration

Expected:

- `query_restaurants` returns restaurant candidates.
- `get_eta_estimate` returns ETA and confidence.
- `get_evidence` returns source links and reviews.
- `record_feedback` writes a feedback row.
- Invalid feedback rating raises an error.

## Report fields

Each recorded agent scenario logs:

- Query.
- Pass/fail status.
- Expected tools.
- Actual tools.
- Tool count.
- System prompt character count, hash, and preview.
- Output quality score.
- Output quality notes.
- Final answer JSON.
- Error detail when present.
