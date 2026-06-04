"""Tool definitions for the restaurant-search ReAct agent."""


TOOLS = [
    {
        "name": "query_restaurants",
        "description": (
            "Search restaurant candidates by location and optional maximum "
            "delivery wait time."
        ),
        "parameters": {
            "type": "object",
            "required": ["location"],
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Area to search, for example Ocean Park 1.",
                },
                "max_wait_time": {
                    "type": "integer",
                    "description": "Maximum acceptable delivery ETA in minutes.",
                },
            },
        },
    },
    {
        "name": "get_eta_estimate",
        "description": "Get predicted delivery ETA and confidence for a restaurant.",
        "parameters": {
            "type": "object",
            "required": ["restaurant_id"],
            "properties": {
                "restaurant_id": {
                    "type": "integer",
                    "description": "Restaurant id returned by query_restaurants.",
                }
            },
        },
    },
    {
        "name": "get_evidence",
        "description": "Fetch source links and review evidence for a restaurant.",
        "parameters": {
            "type": "object",
            "required": ["restaurant_id"],
            "properties": {
                "restaurant_id": {
                    "type": "integer",
                    "description": "Restaurant id to inspect.",
                }
            },
        },
    },
    {
        "name": "record_feedback",
        "description": "Store user feedback for a recommendation.",
        "parameters": {
            "type": "object",
            "required": ["query", "suggestion_id", "user_rating"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Original user query.",
                },
                "suggestion_id": {
                    "type": "integer",
                    "description": "Restaurant id or suggestion id being rated.",
                },
                "user_rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "description": "User rating from 1 to 5.",
                },
                "feedback_text": {
                    "type": "string",
                    "description": "Optional free-text feedback.",
                },
            },
        },
    },
    {
        "name": "clarify",
        "description": "Ask the user a focused clarification question.",
        "parameters": {
            "type": "object",
            "required": ["question"],
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question to ask before continuing.",
                }
            },
        },
    },
]


def get_tool_definitions():
    """Return all tool definitions as JSON-serializable dictionaries."""
    return TOOLS
