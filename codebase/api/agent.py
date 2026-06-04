import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env from codebase root
_CODEBASE_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_CODEBASE_ROOT / ".env")

from api.providers.openrouter_provider import OpenRouterProvider
from api.tool_runners import execute_tool
from api.tools import get_tool_definitions


class ReActAgent:
    """Small ReAct agent for restaurant search and feedback workflows."""

    def __init__(self, provider=None, max_steps=8):
        self.provider = provider or OpenRouterProvider()
        self.max_steps = max_steps
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self):
        prompt_path = Path(__file__).resolve().parent.parent / "artifacts" / "system_prompt.md"
        base_prompt = ""
        if prompt_path.exists():
            base_prompt = prompt_path.read_text(encoding="utf-8")
        else:
            base_prompt = "You are an AI assistant using the ReAct framework."

        # Append tool definitions so the LLM knows exact schemas
        tool_defs = get_tool_definitions()
        tools_json = json.dumps(tool_defs, indent=2, ensure_ascii=False)
        return f"{base_prompt}\n\n## Tool Schemas (JSON)\n{tools_json}"

    def _extract_json(self, text):
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def _parse_model_response(self, response_text):
        json_str = self._extract_json(response_text)
        parsed = json.loads(json_str)
        if not isinstance(parsed, dict):
            raise ValueError("LLM response must be a JSON object")
        return json_str, parsed

    def run(self, user_query, location="Ocean Park 1"):
        user_message = f"User Query: {user_query}\nLocation: {location}"
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        action_trace = []
        step_count = 1

        for _ in range(self.max_steps):
            try:
                response_text = self.provider.chat_completion(messages)
                json_str, parsed = self._parse_model_response(response_text)
            except ValueError as exc:
                return {
                    "query": user_query,
                    "action_trace": action_trace,
                    "error": str(exc),
                }
            except Exception as exc:
                return {
                    "query": user_query,
                    "action_trace": action_trace,
                    "error": f"Failed to parse LLM response: {exc}",
                }

            thought = parsed.get("thought")
            if thought:
                action_trace.append(
                    {"step": step_count, "type": "think", "thought": thought}
                )
                step_count += 1

            if "tool" in parsed:
                tool_name = parsed["tool"]
                params = parsed.get("params", {})
                try:
                    tool_result = execute_tool(tool_name, params)
                except Exception as exc:
                    tool_result = {"error": str(exc)}

                action_trace.append(
                    {
                        "step": step_count,
                        "type": "action",
                        "tool": tool_name,
                        "params": params,
                        "result": tool_result,
                    }
                )
                step_count += 1

                messages.append({"role": "assistant", "content": json_str})
                messages.append(
                    {
                        "role": "user",
                        "content": "Tool Result: "
                        + json.dumps(tool_result, ensure_ascii=False),
                    }
                )
                continue

            if "final_answer" in parsed:
                return {
                    "query": user_query,
                    "action_trace": action_trace,
                    "final_answer": parsed["final_answer"],
                }

            messages.append({"role": "assistant", "content": json_str})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Error: return JSON with either a 'tool' call or "
                        "a 'final_answer'."
                    ),
                }
            )

        return {
            "query": user_query,
            "action_trace": action_trace,
            "error": "Agent stopped after reaching maximum steps.",
        }


if __name__ == "__main__":
    agent = ReActAgent()
    result = agent.run("Giao nhanh ở Ocean Park 1")
    print(json.dumps(result, indent=2, ensure_ascii=False))
