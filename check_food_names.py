import json

def check_food_names():
    """Check all food names in the database."""
    
    print("📖 Reading nutrition database...\n")
    
    with open("data/nutrition_db.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    foods = data.get('foods', [])
    print(f"Total foods: {len(foods)}\n")
    print("=" * 80)
    
    # Show first 20 foods
    print("First 20 foods in database:\n")
    for i, food in enumerate(foods[:20]):
        name = food.get('name', 'N/A')
        aliases = food.get('aliases', [])
        aliases_str = ", ".join(aliases) if aliases else "None"
        
        print(f"{i+1:3d}. Name: {name}")
        print(f"     Aliases: {aliases_str}")
        print(f"     Calories: {food.get('calories', 'N/A')} kcal")
        print()
    
    # Search for specific foods
    print("=" * 80)
    print("\n🔍 Searching for 'tea' related foods:\n")
    
    for food in foods:
        name = food.get('name', '').lower()
        if 'tea' in name:
            print(f"  • {food['name']}")
            print(f"    Aliases: {food.get('aliases', [])}")
            print()
    
    print("\n🔍 Searching for 'coffee' related foods:\n")
    
    for food in foods:
        name = food.get('name', '').lower()
        if 'coffee' in name:
            print(f"  • {food['name']}")
            print(f"    Aliases: {food.get('aliases', [])}")
            print()
    
    print("\n🔍 Searching for 'lemonade':\n")
    
    for food in foods:
        name = food.get('name', '').lower()
        if 'lemonade' in name or 'lemon' in name:
            print(f"  • {food['name']}")
            print(f"    Aliases: {food.get('aliases', [])}")
            print()

if __name__ == "__main__":
    check_food_names()