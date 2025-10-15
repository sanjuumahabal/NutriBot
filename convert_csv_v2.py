import pandas as pd
import json
import re

def create_aliases(dish_name):
    """Create smart aliases for a dish name."""
    
    aliases = []
    original = dish_name.strip()
    
    # Add lowercase version
    aliases.append(original.lower())
    
    # Extract content from parentheses
    if '(' in original and ')' in original:
        # Get text before parentheses
        before_paren = original.split('(')[0].strip()
        aliases.append(before_paren.lower())
        
        # Get text inside parentheses
        inside_paren = re.findall(r'\((.*?)\)', original)
        for text in inside_paren:
            aliases.append(text.strip().lower())
    
    # Split by common separators and add variations
    for separator in [' with ', ' and ', ' or ', ' / ', '-']:
        if separator in original.lower():
            parts = original.lower().split(separator)
            for part in parts:
                cleaned = part.strip()
                if len(cleaned) > 3:  # Skip very short parts
                    aliases.append(cleaned)
    
    # Add individual important words (longer than 3 chars)
    words = original.lower().split()
    important_words = [w for w in words if len(w) > 3 and w not in ['with', 'and', 'the', 'for']]
    aliases.extend(important_words)
    
    # Remove duplicates and empty strings
    aliases = list(set([a for a in aliases if a]))
    
    # Remove the main name if it's in aliases
    main_name = original.lower()
    if main_name in aliases:
        aliases.remove(main_name)
    
    return aliases

def convert_csv_to_db(csv_file, output_file):
    """Convert CSV to nutrition database with better name handling."""
    
    print(f"📖 Reading {csv_file}...\n")
    
    df = pd.read_csv(csv_file)
    print(f"✓ Found {len(df)} dishes\n")
    
    foods = []
    
    for idx, row in df.iterrows():
        dish_name = str(row['Dish Name']).strip()
        
        # Use the full dish name (in lowercase)
        main_name = dish_name.lower()
        
        # Create comprehensive aliases
        aliases = create_aliases(dish_name)
        
        # Create food entry
        food_entry = {
            "id": idx + 1,
            "name": main_name,
            "aliases": aliases,
            "serving_size": "1 serving (100g)",
            "serving_size_grams": 100,
            "calories": round(float(row['Calories (kcal)']), 1),
            "protein": round(float(row['Protein (g)']), 1),
            "carbs": round(float(row['Carbohydrates (g)']), 1),
            "fats": round(float(row['Fats (g)']), 1),
            "fiber": round(float(row['Fibre (g)']), 1)
        }
        
        foods.append(food_entry)
        
        # Show progress for first few entries
        if idx < 5:
            print(f"✓ {food_entry['name']}")
            print(f"  Aliases: {', '.join(aliases[:5])}{'...' if len(aliases) > 5 else ''}")
            print()
    
    print(f"\n✓ Converted {len(foods)} dishes")
    
    # Save to JSON
    output_data = {"foods": foods}
    
    print(f"\n💾 Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Done!\n")
    
    # Test search
    print("🧪 Testing some searches:")
    test_foods = ['hot tea', 'tea', 'chai', 'coffee', 'lemonade']
    
    for search_term in test_foods:
        found = []
        for food in foods:
            if search_term.lower() in food['name'] or search_term.lower() in food.get('aliases', []):
                found.append(food['name'])
        
        if found:
            print(f"  ✓ '{search_term}' found: {found[:3]}")
        else:
            print(f"  ✗ '{search_term}' not found")

if __name__ == "__main__":
    convert_csv_to_db(
        csv_file="data/indian_food_nutrition.csv",
        output_file="data/nutrition_db.json"
    )