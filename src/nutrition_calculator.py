from typing import Dict, List, Optional
from src.database import NutritionDatabase


class NutritionCalculator:
    """Calculate nutritional values for meals."""
    
    def __init__(self, database: NutritionDatabase):
        self.db = database
    
    def calculate_meal(self, parsed_meal: Dict) -> Dict:
        """
        Calculate total nutrition for a parsed meal.
        
        Args:
            parsed_meal: Dict with meal_type and items from parser
            
        Returns:
            Dict with detailed nutrition breakdown
        """
        meal_type = parsed_meal.get('meal_type', 'unknown')
        items = parsed_meal.get('items', [])
        
        if not items:
            return {
                'meal_type': meal_type,
                'items': [],
                'totals': self._get_empty_totals(),
                'status': 'error',
                'message': 'No food items found'
            }
        
        calculated_items = []
        total_nutrition = self._get_empty_totals()
        
        for item in items:
            food_name = item.get('food', '')
            quantity = item.get('quantity', 1)
            unit = item.get('unit', 'serving')
            
            # Find food in database
            food_data = self.db.find_food(food_name)
            
            if not food_data:
                calculated_items.append({
                    'food': food_name,
                    'quantity': quantity,
                    'unit': unit,
                    'status': 'not_found',
                    'message': f'"{food_name}" not found in database'
                })
                continue
            
            # Calculate nutrition based on quantity
            multiplier = self._get_multiplier(quantity, unit, food_data)
            
            item_nutrition = {
                'food': food_data['name'],
                'quantity': quantity,
                'unit': unit,
                'serving_info': food_data['serving_size'],
                'calories': round(food_data['calories'] * multiplier, 1),
                'protein': round(food_data['protein'] * multiplier, 1),
                'carbs': round(food_data['carbs'] * multiplier, 1),
                'fats': round(food_data['fats'] * multiplier, 1),
                'fiber': round(food_data['fiber'] * multiplier, 1),
                'status': 'success'
            }
            
            calculated_items.append(item_nutrition)
            
            # Add to totals
            total_nutrition['calories'] += item_nutrition['calories']
            total_nutrition['protein'] += item_nutrition['protein']
            total_nutrition['carbs'] += item_nutrition['carbs']
            total_nutrition['fats'] += item_nutrition['fats']
            total_nutrition['fiber'] += item_nutrition['fiber']
        
        # Round totals
        for key in total_nutrition:
            total_nutrition[key] = round(total_nutrition[key], 1)
        
        return {
            'meal_type': meal_type,
            'items': calculated_items,
            'totals': total_nutrition,
            'status': 'success'
        }
    
    def _get_multiplier(self, quantity: float, unit: str, food_data: Dict) -> float:
        """
        Calculate multiplier based on quantity and unit.
        
        This is a simplified version. In production, you'd want more 
        sophisticated unit conversion.
        """
        # For most items, quantity directly represents servings
        # e.g., 2 chapatis = 2 servings, 1 bowl = 1 serving
        return quantity
    
    def _get_empty_totals(self) -> Dict:
        """Return empty nutrition totals."""
        return {
            'calories': 0.0,
            'protein': 0.0,
            'carbs': 0.0,
            'fats': 0.0,
            'fiber': 0.0
        }
    
    def format_result(self, result: Dict, format_type: str = 'table') -> str:
        """
        Format calculation results for display.
        
        Args:
            result: Result dict from calculate_meal()
            format_type: 'table' or 'simple'
        """
        if result['status'] == 'error':
            return f"❌ {result.get('message', 'Unknown error')}"
        
        output = []
        output.append(f"\n🍽️  Meal: {result['meal_type'].upper()}")
        output.append("=" * 70)
        
        # Items breakdown
        if format_type == 'table':
            output.append(f"\n{'Food Item':<20} {'Qty':<12} {'Calories':<10} {'Protein':<10} {'Carbs':<10} {'Fats':<8}")
            output.append("-" * 70)
            
            for item in result['items']:
                if item['status'] == 'not_found':
                    output.append(f"{item['food']:<20} {'N/A':<12} ❌ Not found in database")
                else:
                    qty_str = f"{item['quantity']} {item['unit']}"
                    output.append(
                        f"{item['food']:<20} {qty_str:<12} "
                        f"{item['calories']:<10.1f} {item['protein']:<10.1f}g "
                        f"{item['carbs']:<10.1f}g {item['fats']:<8.1f}g"
                    )
        else:
            for item in result['items']:
                if item['status'] == 'not_found':
                    output.append(f"  ❌ {item['food']}: Not found")
                else:
                    output.append(f"  ✓ {item['food']} ({item['quantity']} {item['unit']})")
        
        # Totals
        output.append("-" * 70)
        totals = result['totals']
        output.append(
            f"{'TOTAL':<20} {'':<12} "
            f"{totals['calories']:<10.1f} {totals['protein']:<10.1f}g "
            f"{totals['carbs']:<10.1f}g {totals['fats']:<8.1f}g"
        )
        output.append("=" * 70)
        
        # Summary
        output.append(f"\n📊 Nutrition Summary:")
        output.append(f"   Calories: {totals['calories']} kcal")
        output.append(f"   Protein:  {totals['protein']}g")
        output.append(f"   Carbs:    {totals['carbs']}g")
        output.append(f"   Fats:     {totals['fats']}g")
        output.append(f"   Fiber:    {totals['fiber']}g")
        
        return "\n".join(output)


# Example usage
if __name__ == "__main__":
    from database import NutritionDatabase
    
    db = NutritionDatabase()
    calculator = NutritionCalculator(db)
    
    # Test with sample parsed meal
    sample_meal = {
        "meal_type": "lunch",
        "items": [
            {"food": "chapati", "quantity": 2, "unit": "pieces"},
            {"food": "rice", "quantity": 1, "unit": "bowl"},
            {"food": "daal", "quantity": 1, "unit": "bowl"},
            {"food": "bhindi", "quantity": 1, "unit": "serving"}
        ]
    }
    
    result = calculator.calculate_meal(sample_meal)
    print(calculator.format_result(result))