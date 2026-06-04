# ReAct Agent Test Report

Generated at: 2026-06-04T16:13:39
Total pytest cases: 4
Passed: 4
Failed: 0
Skipped: 0
Recorded agent scenarios: 2

## Scenario Summary

### fast_delivery_ocean_park_react_flow

- Query: Giao nhanh ở Ocean Park 1
- Status: pass
- Expected tools: query_restaurants, get_eta_estimate
- Actual tools: query_restaurants, get_eta_estimate
- Tool count: 2
- System prompt chars: 4315
- System prompt hash: 0e74a1eb48f6
- System prompt preview: You are a ReAct restaurant-search agent.  Your job is to help users find restaurants, estimate delivery time, inspect evidence, record feedback, or ask for clarification.  Always respond with exactly one JSON object. Do not include markdown or extra prose.  For reasoning plus a tool call, use:  {   
- Output quality score: 95/100
- Output quality notes: Uses search and ETA verification before final recommendation.

Final answer:

```json
{
  "suggestions": [
    {
      "id": 1,
      "name": "Quán A - Phở Nhanh Ocean",
      "eta": 32,
      "confidence": 0.85,
      "reason": "Gần Ocean Park 1 và giao trong khoảng 32 phút."
    }
  ]
}
```

### clarify_when_location_is_missing

- Query: Gợi ý quán sushi giao nhanh
- Status: pass
- Expected tools: clarify
- Actual tools: clarify
- Tool count: 1
- System prompt chars: 4315
- System prompt hash: 0e74a1eb48f6
- System prompt preview: You are a ReAct restaurant-search agent.  Your job is to help users find restaurants, estimate delivery time, inspect evidence, record feedback, or ask for clarification.  Always respond with exactly one JSON object. Do not include markdown or extra prose.  For reasoning plus a tool call, use:  {   
- Output quality score: 90/100
- Output quality notes: Does not guess location and asks a focused clarification.

Final answer:

```json
{
  "clarification_question": "Bạn muốn tìm sushi ở khu vực nào?"
}
```
