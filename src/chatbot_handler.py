import os
import json
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class NutritionChatbot:
    """Conversational chatbot that handles both casual chat and nutrition analysis."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("Gemini API key not found.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        # System prompt for the chatbot personality
        self.system_prompt = """You are NutriBot, a friendly and knowledgeable nutrition assistant chatbot. 

Your personality:
- Warm, encouraging, and supportive
- Expert in nutrition and healthy eating
- Casual and conversational, but professional
- Use emojis occasionally to be friendly (but not excessive)
- Give brief, helpful responses

Your capabilities:
1. CASUAL CONVERSATION: Greet users, answer questions about nutrition, give tips, be friendly
2. MEAL ANALYSIS: When user describes what they ate, identify it and respond that you'll analyze it

How to respond:
- If user greets (hi, hello, hey): Greet back warmly and introduce yourself
- If user asks general questions: Answer briefly and helpfully
- If user describes a MEAL they ate: Respond in this EXACT format:
  {
    "type": "meal_analysis",
    "message": "Great! Let me analyze that for you 🍽️",
    "meal_description": "exact text of what they ate"
  }
- For anything else: Have a friendly conversation

Examples:
User: "Hi"
You: "Hello! 👋 I'm NutriBot, your personal nutrition assistant! I can help you track your meals and understand what you're eating. Just tell me what you had for breakfast, lunch, or dinner, and I'll break down the nutrition for you! How can I help you today?"

User: "What's a healthy breakfast?"
You: "A healthy breakfast should include protein, complex carbs, and some healthy fats! 🍳 Some great options are: oatmeal with nuts and fruits, whole grain toast with eggs, or idli with sambar. Want me to analyze your breakfast?"

User: "I had 2 chapatis and dal for lunch"
You: {
  "type": "meal_analysis",
  "message": "Perfect! Let me analyze your lunch 🍽️",
  "meal_description": "2 chapatis and dal for lunch"
}

User: "How many calories should I eat?"
You: "That depends on your age, gender, activity level, and goals! 💪 Generally, adults need 1800-2500 calories per day. Want to track your meals so we can see how you're doing?"

IMPORTANT: When user mentions eating something (had, ate, eating, consumed, etc.), ALWAYS use the meal_analysis format.
"""
    
    def classify_intent(self, user_message: str) -> Dict:
        """
        Determine if the message is a meal description or casual conversation.
        """
        # Keywords that indicate meal description
        meal_keywords = [
            'had', 'ate', 'eating', 'eaten', 'consumed', 'drink', 'drank',
            'breakfast', 'lunch', 'dinner', 'snack', 'meal',
            'chapati', 'roti', 'rice', 'dal', 'daal', 'curry', 'sabzi'
        ]
        
        user_lower = user_message.lower()
        
        # Check if it's likely a meal description
        has_meal_keyword = any(keyword in user_lower for keyword in meal_keywords)
        
        # Check if it has food quantities
        has_quantity = any(char.isdigit() for char in user_message)
        
        if has_meal_keyword or (has_quantity and len(user_message.split()) > 3):
            return {"type": "potential_meal", "confidence": "high"}
        
        return {"type": "conversation", "confidence": "high"}
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> Dict:
        """
        Main chat function that handles both conversation and meal analysis.
        
        Args:
            user_message: User's input
            conversation_history: List of previous messages
            
        Returns:
            Dict with response and type
        """
        if conversation_history is None:
            conversation_history = []
        
        # Quick intent check first (no API call)
        intent = self.classify_intent(user_message)
        
        # If it's clearly a meal, skip the chat API call and go straight to parsing
        if intent['type'] == 'potential_meal':
            return {
                "type": "meal_analysis",
                "message": "Let me analyze that for you!",
                "meal_description": user_message,
                "raw_response": ""
            }
        
        # Otherwise, do regular conversation
        context = self.system_prompt + "\n\nConversation:\n"
        
        for msg in conversation_history[-5:]:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            context += f"{role.title()}: {content}\n"
        
        context += f"User: {user_message}\nYou:"
        
        try:
            response = self.model.generate_content(context)
            response_text = response.text.strip()
            
            # Try to parse as JSON (for meal analysis)
            if '{' in response_text and '"type": "meal_analysis"' in response_text:
                json_start = response_text.index('{')
                json_end = response_text.rindex('}') + 1
                json_str = response_text[json_start:json_end]
                
                try:
                    parsed = json.loads(json_str)
                    return {
                        "type": "meal_analysis",
                        "message": parsed.get("message", "Let me analyze that!"),
                        "meal_description": parsed.get("meal_description", user_message),
                        "raw_response": response_text
                    }
                except json.JSONDecodeError:
                    pass
            
            # Regular conversation response
            return {
                "type": "conversation",
                "message": response_text,
                "raw_response": response_text
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"Sorry, I encountered an error: {str(e)}",
                "raw_response": ""
            }
    
    def generate_nutrition_response(self, result: Dict) -> str:
        """
        Generate a friendly response after nutrition analysis.
        Quick, without API call for simple cases.
        
        Args:
            result: Nutrition calculation result
            
        Returns:
            Friendly message about the meal
        """
        totals = result['totals']
        meal_type = result['meal_type']
        protein = totals['protein']
        calories = totals['calories']
        
        # Simple rule-based responses (no API call needed)
        if protein > 20:
            return f"Excellent! Your {meal_type} packs {protein:.0f}g of protein - great for muscle health! 💪"
        elif protein > 10:
            return f"Nice {meal_type}! You're getting {calories:.0f} calories and {protein:.0f}g protein. 👍"
        elif calories < 200:
            return f"That's a light {meal_type} with {calories:.0f} calories. Consider adding some protein! 🥗"
        else:
            return f"Your {meal_type} has {calories:.0f} calories and {protein:.0f}g protein. Looking good! 😊"


# Example usage
if __name__ == "__main__":
    chatbot = NutritionChatbot()
    
    # Test conversation
    test_messages = [
        "Hi there!",
        "What should I eat for breakfast?",
        "I had 2 chapatis and dal for lunch",
        "Thanks!"
    ]
    
    conversation = []
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = chatbot.chat(msg, conversation)
        print(f"Bot: {response['message']}")
        print(f"Type: {response['type']}")
        
        # Add to conversation history
        conversation.append({"role": "user", "content": msg})
        conversation.append({"role": "assistant", "content": response['message']})