import os
import json
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MealParser:
    """Parses meal descriptions using Google Gemini API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Gemini parser.
        
        Args:
            api_key: Gemini API key. If None, loads from GEMINI_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def parse_meal(self, user_input: str) -> Dict:
        """
        Parse user's meal description into structured format.
        
        Args:
            user_input: Natural language meal description
            
        Returns:
            Dict with meal_type and items list
        """
        prompt = f"""
You are a nutrition assistant. Extract food items and quantities from the user's meal description.

User input: "{user_input}"

Extract and return ONLY a valid JSON object (no other text) with this exact structure:
{{
  "meal_type": "breakfast|lunch|dinner|snack",
  "items": [
    {{
      "food": "food name in lowercase",
      "quantity": numeric_value,
      "unit": "pieces|bowl|serving|glass|grams|cup"
    }}
  ]
}}

Rules:
1. Normalize food names (e.g., "rotis" → "chapati", "chawal" → "rice")
2. If meal type is not mentioned, use "lunch" as default
3. Use standard units: pieces for countable items, bowl for liquids/curries, serving for vegetables
4. Quantity should be a number (convert "a couple" → 2, "half" → 0.5)
5. Return ONLY the JSON, no other text or explanation

Example:
Input: "I had 2 rotis and daal for dinner"
Output: {{"meal_type": "dinner", "items": [{{"food": "chapati", "quantity": 2, "unit": "pieces"}}, {{"food": "daal", "quantity": 1, "unit": "bowl"}}]}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            parsed_data = json.loads(response_text)
            
            # Validate structure
            if 'meal_type' not in parsed_data or 'items' not in parsed_data:
                raise ValueError("Invalid response structure from Gemini")
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse Gemini response as JSON: {e}")
            print(f"Response was: {response_text}")
            return self._get_fallback_response()
        except Exception as e:
            print(f"✗ Error calling Gemini API: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> Dict:
        """Return a fallback response when parsing fails."""
        return {
            "meal_type": "unknown",
            "items": [],
            "error": "Failed to parse meal description"
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the parser
    parser = MealParser()
    
    test_inputs = [
        "I had 2 chapatis, 1 bowl of rice, daal and bhindi for lunch",
        "Ate 3 idlis with sambar for breakfast",
        "Had chicken curry with 2 rotis for dinner"
    ]
    
    print("--- Testing Meal Parser ---\n")
    for test_input in test_inputs:
        print(f"Input: {test_input}")
        result = parser.parse_meal(test_input)
        print(f"Output: {json.dumps(result, indent=2)}")
        print("-" * 50)