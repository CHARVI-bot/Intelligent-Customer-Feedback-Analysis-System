# Simple mock intelligent analyzer 
# In a real-world scenario, you would integrate with an LLM via API (e.g., Google Gemini, OpenAI)
# to perform advanced sentiment analysis and topic extraction.

def analyze_text(text: str, rating: int) -> dict:
    text_lower = text.lower()
    
    # Determine Sentiment
    sentiment_score = rating / 5.0  # basic correlation
    sentiment = "Neutral"
    if rating >= 4 or any(word in text_lower for word in ["great", "excellent", "good", "amazing", "love"]):
        sentiment = "Positive"
        sentiment_score = max(sentiment_score, 0.8)
    elif rating <= 2 or any(word in text_lower for word in ["bad", "poor", "terrible", "hate", "awful", "worst"]):
        sentiment = "Negative"
        sentiment_score = min(sentiment_score, 0.3)
    
    # Determine Themes
    themes = []
    if any(word in text_lower for word in ["support", "service", "help", "agent"]): 
        themes.append("Customer Service")
    if any(word in text_lower for word in ["price", "cost", "expensive", "cheap", "value"]): 
        themes.append("Pricing")
    if any(word in text_lower for word in ["ui", "interface", "design", "look", "feel"]): 
        themes.append("User Interface")
    if any(word in text_lower for word in ["fast", "slow", "speed", "performance", "lag"]): 
        themes.append("Performance")
    if any(word in text_lower for word in ["bug", "crash", "error", "broken", "issue"]): 
        themes.append("Reliability")
    
    if not themes:
        themes.append("General")
        
    # Determine Urgency
    urgency = "Low"
    if sentiment == "Negative" and any(word in text_lower for word in ["cancel", "refund", "urgent", "asap", "lawsuit", "manager"]):
        urgency = "High"
    elif sentiment == "Negative":
        urgency = "Medium"
        
    return {
        "sentiment": sentiment,
        "sentiment_score": round(sentiment_score, 2),
        "themes": themes,
        "urgency": urgency
    }
