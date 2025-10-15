import pandas as pd

def preview_csv(csv_file):
    """Preview CSV content before conversion."""
    
    print("📖 Reading CSV file...\n")
    
    try:
        df = pd.read_csv(csv_file)
        
        print(f"✓ Found {len(df)} rows")
        print(f"✓ Columns: {list(df.columns)}\n")
        
        print("=" * 100)
        print("First 10 rows:\n")
        
        for idx, row in df.head(10).iterrows():
            print(f"{idx + 1}. Dish: {row['Dish Name']}")
            print(f"   Calories: {row['Calories (kcal)']} kcal")
            print(f"   Protein: {row['Protein (g)']}g | Carbs: {row['Carbohydrates (g)']}g | Fats: {row['Fats (g)']}g")
            print()
        
        print("=" * 100)
        print("\n🔍 Checking for duplicates...\n")
        
        # Check dish names
        dish_names = df['Dish Name'].tolist()
        unique_dishes = set(dish_names)
        
        print(f"Total dishes: {len(dish_names)}")
        print(f"Unique dishes: {len(unique_dishes)}")
        
        if len(dish_names) != len(unique_dishes):
            print("\n⚠️  Warning: Found duplicate dish names!")
            
            # Show duplicates
            from collections import Counter
            duplicates = [name for name, count in Counter(dish_names).items() if count > 1]
            
            print("\nDuplicate dishes:")
            for dup in duplicates[:10]:
                count = dish_names.count(dup)
                print(f"  • '{dup}' appears {count} times")
        
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        print("\nMake sure your CSV file is in the correct location.")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

if __name__ == "__main__":
    # Update this to your actual CSV filename
    preview_csv("data/indian_food_nutrition.csv")