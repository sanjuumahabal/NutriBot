#!/usr/bin/env python3
"""
Nutrition Chatbot - CLI Version
Main application file
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from database import NutritionDatabase
from nlp_parser import MealParser
from nutrition_calculator import NutritionCalculator


class NutritionChatbot:
    """Main chatbot application."""
    
    def __init__(self):
        print("🔧 Initializing Nutrition Chatbot...")
        
        try:
            # Initialize components
            self.db = NutritionDatabase()
            self.parser = MealParser()
            self.calculator = NutritionCalculator(self.db)
            
            print("✓ All components loaded successfully!\n")
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            sys.exit(1)
    
    def process_meal(self, user_input: str) -> str:
        """
        Process a meal description and return nutrition info.
        
        Args:
            user_input: User's meal description
            
        Returns:
            Formatted nutrition information
        """
        print("\n⏳ Analyzing your meal...")
        
        # Step 1: Parse the input
        parsed_meal = self.parser.parse_meal(user_input)
        
        if 'error' in parsed_meal:
            return f"❌ Error: {parsed_meal['error']}"
        
        # Step 2: Calculate nutrition
        result = self.calculator.calculate_meal(parsed_meal)
        
        # Step 3: Format and return
        return self.calculator.format_result(result)
    
    def run_interactive(self):
        """Run the chatbot in interactive mode."""
        print("=" * 70)
        print("🥗 NUTRITION CHATBOT")
        print("=" * 70)
        print("\nTell me what you ate, and I'll calculate the nutrition!")
        print("Examples:")
        print("  • I had 2 chapatis, 1 bowl of rice, daal and bhindi for lunch")
        print("  • Ate 3 idlis with sambar for breakfast")
        print("  • Had chicken curry with 2 rotis")
        print("\nCommands:")
        print("  • 'quit' or 'exit' - Exit the chatbot")
        print("  • 'foods' - List all available foods")
        print("=" * 70)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using Nutrition Chatbot! Stay healthy!")
                    break
                
                if user_input.lower() == 'foods':
                    self.show_available_foods()
                    continue
                
                # Process meal
                result = self.process_meal(user_input)
                print(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
    
    def show_available_foods(self):
        """Display all available foods in the database."""
        foods = self.db.foods
        
        print("\n📋 Available Foods in Database:")
        print("=" * 70)
        
        for i, food in enumerate(foods, 1):
            aliases = ", ".join(food['aliases'][:3]) if food['aliases'] else "No aliases"
            print(f"{i:2d}. {food['name'].title():<20} (aka: {aliases})")
        
        print(f"\nTotal: {len(foods)} foods")


def main():
    """Main entry point."""
    # Check if running with arguments
    if len(sys.argv) > 1:
        # Single query mode
        chatbot = NutritionChatbot()
        query = " ".join(sys.argv[1:])
        result = chatbot.process_meal(query)
        print(result)
    else:
        # Interactive mode
        chatbot = NutritionChatbot()
        chatbot.run_interactive()


if __name__ == "__main__":
    main()