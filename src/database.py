import json
from typing import List, Dict, Optional
from pathlib import Path


class NutritionDatabase:
    """Handles loading and querying the nutrition database."""
    
    def __init__(self, db_path: str = "data/nutrition_db.json"):
        self.db_path = Path(db_path)
        self.foods: List[Dict] = []
        self.load_database()
    
    def load_database(self):
        """Load the nutrition database from JSON file."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.foods = data.get('foods', [])
            print(f"✓ Loaded {len(self.foods)} foods from database")
        except FileNotFoundError:
            print(f"✗ Database file not found: {self.db_path}")
            self.foods = []
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON in database file: {self.db_path}")
            self.foods = []
    
    def find_food(self, food_name: str) -> Optional[Dict]:
        """
        Find a food item by name or alias.
        Returns the food dict if found, None otherwise.
        """
        food_name_lower = food_name.lower().strip()
        
        for food in self.foods:
            # Check exact name match
            if food['name'].lower() == food_name_lower:
                return food
            
            # Check aliases
            if 'aliases' in food:
                for alias in food['aliases']:
                    if alias.lower() == food_name_lower:
                        return food
        
        return None
    
    def get_all_food_names(self) -> List[str]:
        """Get list of all food names and aliases."""
        names = []
        for food in self.foods:
            names.append(food['name'])
            if 'aliases' in food:
                names.extend(food['aliases'])
        return names
    
    def search_food(self, query: str) -> List[Dict]:
        """
        Search for foods containing the query string.
        Useful for fuzzy matching.
        """
        query_lower = query.lower().strip()
        results = []
        
        for food in self.foods:
            # Check if query is in name
            if query_lower in food['name'].lower():
                results.append(food)
                continue
            
            # Check if query is in any alias
            if 'aliases' in food:
                for alias in food['aliases']:
                    if query_lower in alias.lower():
                        results.append(food)
                        break
        
        return results


# Example usage
if __name__ == "__main__":
    db = NutritionDatabase()
    
    # Test finding foods
    print("\n--- Testing find_food ---")
    chapati = db.find_food("roti")
    if chapati:
        print(f"Found: {chapati['name']}")
        print(f"Calories: {chapati['calories']} per {chapati['serving_size']}")
    
    # Test search
    print("\n--- Testing search_food ---")
    results = db.search_food("dal")
    print(f"Found {len(results)} items matching 'dal':")
    for food in results:
        print(f"  - {food['name']}")