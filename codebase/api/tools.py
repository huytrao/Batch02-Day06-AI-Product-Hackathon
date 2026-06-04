"""
Tool definitions for the restaurant recommendation ReAct agent.
"""

def query_restaurants(location: str, max_wait_time: int) -> list[dict]:
    """
    Search for restaurants in a specific location with a maximum wait time.
    
    Args:
        location: The location to search in (e.g., 'Ocean Park 1').
        max_wait_time: Maximum acceptable delivery wait time in minutes.
        
    Returns:
        List of restaurant candidate dictionaries.
    """
    pass

def get_eta_estimate(restaurant_id: int) -> dict:
    """
    Get the estimated time of arrival (ETA) and confidence score for a specific restaurant.
    
    Args:
        restaurant_id: The ID of the restaurant.
        
    Returns:
        Dictionary containing 'predicted_eta' and 'confidence'.
    """
    pass

def get_evidence(restaurant_id: int) -> dict:
    """
    Get evidence such as source links and reviews for a specific restaurant.
    
    Args:
        restaurant_id: The ID of the restaurant.
        
    Returns:
        Dictionary containing 'source_links' and 'reviews'.
    """
    pass

def record_feedback(query: str, suggestion_id: int, user_rating: int, feedback_text: str) -> dict:
    """
    Record user feedback for a suggestion.
    
    Args:
        query: The original user query.
        suggestion_id: The ID of the accepted suggestion (restaurant).
        user_rating: Rating out of 5.
        feedback_text: Detailed feedback text.
        
    Returns:
        Dictionary with status of the feedback recording.
    """
    pass

def clarify(question: str) -> dict:
    """
    Ask a clarifying question to the user and wait for their response.
    
    Args:
        question: The question to ask the user.
        
    Returns:
        Dictionary containing the user's response (or status indicating waiting for response).
    """
    pass
