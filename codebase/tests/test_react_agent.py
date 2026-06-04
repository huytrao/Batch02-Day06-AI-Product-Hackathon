import json
import time

import pytest

from api.agent import ReActAgent
from api.tool_runners import execute_tool
from conftest import record_agent_case


class FakeProvider:
    def __init__(self, responses):
        self.responses = list(responses)
        self.messages_seen = []
        self.system_prompt_seen = ""

    def chat_completion(self, messages):
        self.messages_seen.append(list(messages))
        self.system_prompt_seen = messages[0]["content"]
        if not self.responses:
            raise AssertionError("FakeProvider has no responses left")
        return json.dumps(self.responses.pop(0), ensure_ascii=False)


def _action_tools(result):
    return [
        step["tool"]
        for step in result.get("action_trace", [])
        if step.get("type") == "action"
    ]


def test_fast_delivery_ocean_park_react_flow(request):
    provider = FakeProvider(
        [
            {
                "thought": "User wants fast delivery near Ocean Park 1, so I need nearby candidates under 45 minutes.",
                "tool": "query_restaurants",
                "params": {"location": "Ocean Park 1", "max_wait_time": 45},
            },
            {
                "thought": "The top candidate has a fast listed ETA, so I should verify its ETA confidence.",
                "tool": "get_eta_estimate",
                "params": {"restaurant_id": 1},
            },
            {
                "thought": "The ETA is fast and confidence is high enough to recommend.",
                "final_answer": {
                    "suggestions": [
                        {
                            "id": 1,
                            "name": "Quán A - Phở Nhanh Ocean",
                            "eta": 32,
                            "confidence": 0.85,
                            "reason": "Gần Ocean Park 1 và giao trong khoảng 32 phút.",
                        }
                    ]
                },
            },
        ]
    )

    start = time.perf_counter()
    result = ReActAgent(provider=provider).run("Giao nhanh ở Ocean Park 1")
    elapsed = time.perf_counter() - start

    record_agent_case(
        request.config,
        case_id="fast_delivery_ocean_park_react_flow",
        user_query="Giao nhanh ở Ocean Park 1",
        result=result,
        provider=provider,
        expected_tools=["query_restaurants", "get_eta_estimate"],
        quality_score=95,
        quality_notes="Uses search and ETA verification before final recommendation.",
    )

    assert elapsed < 2
    assert "error" not in result
    assert _action_tools(result) == ["query_restaurants", "get_eta_estimate"]
    assert len(_action_tools(result)) >= 2
    assert result["action_trace"][1]["params"] == {
        "location": "Ocean Park 1",
        "max_wait_time": 45,
    }
    assert result["action_trace"][1]["result"]
    confidence = result["final_answer"]["suggestions"][0]["confidence"]
    assert 0.0 <= confidence <= 1.0
    assert "Tool Result" in provider.messages_seen[1][-1]["content"]


def test_clarify_when_location_is_missing(request):
    provider = FakeProvider(
        [
            {
                "thought": "The user asks for sushi but did not provide a location.",
                "tool": "clarify",
                "params": {"question": "Bạn muốn tìm sushi ở khu vực nào?"},
            },
            {
                "thought": "I should wait for the user's location before searching.",
                "final_answer": {
                    "clarification_question": "Bạn muốn tìm sushi ở khu vực nào?"
                },
            },
        ]
    )

    result = ReActAgent(provider=provider).run("Gợi ý quán sushi giao nhanh")

    record_agent_case(
        request.config,
        case_id="clarify_when_location_is_missing",
        user_query="Gợi ý quán sushi giao nhanh",
        result=result,
        provider=provider,
        expected_tools=["clarify"],
        quality_score=90,
        quality_notes="Does not guess location and asks a focused clarification.",
    )

    assert "error" not in result
    assert _action_tools(result) == ["clarify"]
    assert result["action_trace"][1]["result"]["needs_clarification"] is True
    assert "clarification_question" in result["final_answer"]


def test_tool_runner_query_eta_evidence_and_feedback():
    candidates = execute_tool(
        "query_restaurants", {"location": "Ocean Park 1", "max_wait_time": 45}
    )
    assert candidates
    assert candidates[0]["location"] == "Ocean Park 1"

    eta = execute_tool("get_eta_estimate", {"restaurant_id": candidates[0]["id"]})
    assert eta["predicted_eta"] is None or eta["predicted_eta"] <= 45
    assert 0.0 <= eta["confidence"] <= 1.0

    evidence = execute_tool("get_evidence", {"restaurant_id": candidates[0]["id"]})
    assert evidence["source_links"]
    assert evidence["reviews"]

    feedback = execute_tool(
        "record_feedback",
        {
            "query": "Giao nhanh ở Ocean Park 1",
            "suggestion_id": candidates[0]["id"],
            "user_rating": 5,
            "feedback_text": "Gợi ý hợp lý.",
        },
    )
    assert feedback["status"] == "recorded"
    assert feedback["feedback_id"] > 0


def test_record_feedback_rejects_invalid_rating():
    with pytest.raises(ValueError):
        execute_tool(
            "record_feedback",
            {
                "query": "Giao nhanh ở Ocean Park 1",
                "suggestion_id": 1,
                "user_rating": 6,
                "feedback_text": "Invalid rating.",
            },
        )
