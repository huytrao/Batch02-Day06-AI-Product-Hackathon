# Agent Testing Guide

## Scope

This guide covers the ReAct restaurant-search agent task:

- `api/agent.py`: ReAct reasoning loop, action selection, tool execution, final answer.
- `api/tools.py`: tool definitions and schemas.
- `api/tool_runners.py`: SQLite-backed tool execution framework.
- `artifacts/tools.yaml`: tool registry.
- `artifacts/system_prompt.md`: ReAct JSON prompt.
- `artifacts/action_trace_example.json`: sample trace output.

## Run tests

From `codebase`:

```bash
python -m pytest -q
```

The test report path is printed at the end:

```text
Logs saved to: <project>/test_logs/react_agent_report_<timestamp>.md
Pass/Fail summary: <passed> passed, <failed> failed, <skipped> skipped
```

## What is tested

The tests validate:

- Sample query `"Giao nhanh ở Ocean Park 1"` completes in under 2 seconds.
- Agent produces a valid `action_trace`.
- Recommendation queries use at least two actions:
  - `query_restaurants`
  - `get_eta_estimate`
- Tool params are correct.
- Tool results are valid SQLite-backed records.
- Confidence is between `0.0` and `1.0`.
- Missing location triggers `clarify`.
- `get_evidence` returns links and review summaries.
- `record_feedback` writes to the feedback table and rejects invalid ratings.

## Tool list

- `query_restaurants(location, max_wait_time)`
- `get_eta_estimate(restaurant_id)`
- `get_evidence(restaurant_id)`
- `record_feedback(query, suggestion_id, user_rating, feedback_text)`
- `clarify(question)`

## Debug checklist

If a test fails, check:

1. The model response is valid JSON.
2. Tool names match `artifacts/tools.yaml`.
3. Tool params match the schema.
4. `execute_tool` returns JSON-serializable values.
5. Confidence values stay in the `0.0` to `1.0` range.
6. The final answer uses restaurant ids returned by tools.
