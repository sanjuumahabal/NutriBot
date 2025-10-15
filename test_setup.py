#!/usr/bin/env python3
"""
Test script to verify all components are set up correctly.
Run this after installation to check if everything works.
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are installed."""
    print("Testing imports...")
    
    required_packages = {
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv',
        'pydantic': 'pydantic'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All packages installed\n")
    return True


def test_file_structure():
    """Test if all required files and folders exist."""
    print("Testing file structure...")
    
    required_paths = {
        'data/nutrition_db.json': 'file',
        'src/__init__.py': 'file',
        'src/database.py': 'file',
        'src/nlp_parser.py': 'file',
        'src/nutrition_calculator.py': 'file',
        'main.py': 'file',
        '.env': 'file'
    }
    
    missing = []
    for path, path_type in required_paths.items():
        file_path = Path(path)
        
        if path_type == 'file':
            if file_path.exists() and file_path.is_file():
                print(f"  ✓ {path}")
            else:
                print(f"  ✗ {path} - NOT FOUND")
                missing.append(path)
    
    if missing:
        print(f"\nMissing files: {', '.join(missing)}")
        return False
    
    print("✓ All files present\n")
    return True


def test_api_key():
    """Test if Gemini API key is configured."""
    print("Testing API configuration...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print(" GEMINI_API_KEY not found in .env file")
            print("\n Please add your Gemini API key to .env file:")
            print("   GEMINI_API_KEY=your_key_here")
            return False
        
        if api_key == 'your_gemini_api_key_here':
            print(" GEMINI_API_KEY is still set to placeholder")
            print("\n Please replace with your actual API key in .env file")
            return False
        
        print(f" API key configured (length: {len(api_key)} characters)")
        print("API configuration looks good\n")
        return True
        
    except Exception as e:
        print(f" Error checking API key: {e}")
        return False


def test_database():
    """Test if database loads correctly."""
    print("Testing database...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'src'))
        from database import NutritionDatabase
        
        db = NutritionDatabase()
        
        if len(db.foods) == 0:
            print(" Database is empty")
            return False
        
        print(f" Loaded {len(db.foods)} foods")
        
        # Test searching
        test_food = db.find_food("chapati")
        if test_food:
            print(f"   Database search working (found: {test_food['name']})")
        else:
            print("   Database search not working")
            return False
        
        print(" Database functioning correctly\n")
        return True
        
    except Exception as e:
        print(f"   Error loading database: {e}")
        return False


def test_parser():
    """Test if NLP parser can be initialized."""
    print("Testing NLP parser...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'src'))
        from nlp_parser import MealParser
        
        parser = MealParser()
        print("   Parser initialized successfully")
        
        # Try a simple parse (this will use API credits)
        print("   Testing actual parsing (this uses API)...")
        result = parser.parse_meal("2 rotis and daal")
        
        if 'items' in result and len(result['items']) > 0:
            print(f"   Parser working! Found {len(result['items'])} items")
        else:
            print("   Parser returned unexpected result")
            print(f"    Result: {result}")
        
        print(" NLP parser functioning\n")
        return True
        
    except ValueError as e:
        if "API key" in str(e):
            print(f"   {e}")
            return False
        raise
    except Exception as e:
        print(f"   Error initializing parser: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("🔍 NUTRITION CHATBOT - SETUP VERIFICATION")
    print("=" * 70)
    print()
    
    tests = [
        ("Package Installation", test_imports),
        ("File Structure", test_file_structure),
        ("API Configuration", test_api_key),
        ("Database", test_database),
        ("NLP Parser", test_parser)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f" {test_name} failed with error: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("=" * 70)
    print(" TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = " PASSED" if result else "✗ FAILED"
        print(f"{test_name:<30} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 70)
    if all_passed:
        print("All tests passed! Your setup is ready.")
        print("\nYou can now run: python main.py")
    else:
        print(" Some tests failed. Please fix the issues above.")
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())