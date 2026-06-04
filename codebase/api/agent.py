"""
ReAct Agent Implementation.
Handles the Reasoning and Acting loop.
"""
from typing import List, Dict, Any, Callable
import json

class ReActAgent:
    def __init__(self, tool_registry: Dict[str, Callable], system_prompt: str = ""):
        self.tool_registry = tool_registry
        self.system_prompt = system_prompt
        self.action_trace = []
        self.step_counter = 1

    def _think(self, thought: str):
        self.action_trace.append({
            "step": self.step_counter,
            "type": "think",
            "thought": thought
        })
        self.step_counter += 1

    def _act(self, tool_name: str, params: Dict[str, Any]) -> Any:
        tool_func = self.tool_registry.get(tool_name)
        if not tool_func:
            result = {"error": f"Tool {tool_name} not found"}
        else:
            try:
                result = tool_func(**params)
            except Exception as e:
                result = {"error": str(e)}
        
        self.action_trace.append({
            "step": self.step_counter,
            "type": "action",
            "tool": tool_name,
            "params": params,
            "result": result
        })
        self.step_counter += 1
        return result

    def run(self, query: str) -> Dict[str, Any]:
        """
        Mocking the LLM reasoning loop.
        In a real scenario, an LLM would generate the thoughts and tool calls based on the system prompt and history.
        Here we hardcode the sequence to demonstrate the ReAct pattern for the specific use case.
        """
        self.action_trace = []
        self.step_counter = 1
        
        # ReAct Loop Simulation
        self._think(f"User query: '{query}'. I need to extract location and requirements.")
        self._think("Extracted location: 'Ocean Park 1'. Requirement: 'fast delivery' (e.g., max 45 mins wait time). I should query restaurants.")
        
        restaurants = self._act("query_restaurants", {"location": "Ocean Park 1", "max_wait_time": 45})
        
        self._think(f"Found {len(restaurants)} candidate restaurants. I need to get accurate ETA estimates for them.")
        
        best_suggestions = []
        for rest in restaurants:
            eta_info = self._act("get_eta_estimate", {"restaurant_id": rest["id"]})
            if "predicted_eta" in eta_info:
                best_suggestions.append({
                    "id": rest["id"],
                    "name": rest["name"],
                    "eta": eta_info["predicted_eta"],
                    "confidence": eta_info.get("confidence", 0.0)
                })
        
        # Sort by lowest ETA
        best_suggestions.sort(key=lambda x: x["eta"])
        
        if best_suggestions:
            self._think(f"Evaluated ETAs. The best suggestion is '{best_suggestions[0]['name']}' with an ETA of {best_suggestions[0]['eta']} minutes. I will construct the final answer.")
            final_answer = {"suggestions": best_suggestions}
        else:
            self._think("No suitable restaurants found meeting the criteria. I will ask the user to modify the requirements.")
            final_answer = {"suggestions": []}
            
        return {
            "query": query,
            "action_trace": self.action_trace,
            "final_answer": final_answer
        }

if __name__ == "__main__":
    # Simple manual test
    from tool_runners import TOOL_RUNNERS
    agent = ReActAgent(tool_registry=TOOL_RUNNERS)
    result = agent.run("Giao nhanh ở Ocean Park 1")
    print(json.dumps(result, indent=2, ensure_ascii=False))
