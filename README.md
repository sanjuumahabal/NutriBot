# 🥗 Nutrition Chatbot

An intelligent chatbot that analyzes meal descriptions and provides detailed nutritional information including calories, proteins, carbs, fats, and fiber.

## 🌟 Features

- **Natural Language Processing**: Understands casual meal descriptions using Google Gemini AI
- **Indian Food Focus**: Comprehensive database of common Indian foods
- **Detailed Nutrition Breakdown**: Calories, protein, carbs, fats, and fiber per meal
- **Flexible Input**: Handles various ways of describing food and quantities
- **Interactive CLI**: User-friendly command-line interface

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

## 🚀 Setup Instructions

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Clone/Create Project Structure

Create the following folder structure:

```
nutrition-chatbot/
├── data/
│   └── nutrition_db.json
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── nlp_parser.py
│   └── nutrition_calculator.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

### Step 3: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Create a `.env` file in the root directory
2. Add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Create Empty `__init__.py`

Create an empty file at `src/__init__.py`:

```bash
# On Windows:
type nul > src\__init__.py

# On macOS/Linux:
touch src/__init__.py
```

## 🎯 Usage

### Interactive Mode

Run the chatbot in interactive mode:

```bash
python main.py
```

Then type your meals naturally:

```
💬 You: I had 2 chapatis, 1 bowl of rice, daal and bhindi for lunch
💬 You: Ate 3 idlis with sambar for breakfast
💬 You: Had chicken curry with 2 rotis
```

### Single Query Mode

Process a single meal description:

```bash
python main.py "I had 2 chapatis and daal for lunch"
```

### Available Commands

While in interactive mode:
- `foods` - List all available foods in the database
- `quit` or `exit` - Exit the chatbot

## 📊 Example Output

```
🍽️  Meal: LUNCH
======================================================================

Food Item            Qty          Calories   Protein    Carbs      Fats    
----------------------------------------------------------------------
chapati              2 pieces     140.0      5.0g       30.0g      0.8g    
rice                 1 bowl       200.0      4.2g       45.0g      0.4g    
daal                 1 bowl       120.0      9.0g       20.0g      0.5g    
bhindi               1 serving    50.0       2.0g       10.0g      0.2g    
----------------------------------------------------------------------
TOTAL                             510.0      20.2g      105.0g     1.9g    
======================================================================

📊 Nutrition Summary:
   Calories: 510.0 kcal
   Protein:  20.2g
   Carbs:    105.0g
   Fats:     1.9g
   Fiber:    14.1g
```

## 🍛 Available Foods

The database currently includes 15 common Indian foods:
- Chapati/Roti/Phulka
- Rice (White/Plain)
- Daal/Lentils
- Bhindi (Okra)
- Paneer
- Chicken Curry
- Aloo Sabzi
- Curd/Yogurt
- Paratha
- Egg
- Idli
- Dosa
- Sambar
- Rajma
- Milk

You can easily add more foods by editing `data/nutrition_db.json`.

## 🔧 Project Structure

```
nutrition-chatbot/
├── data/
│   └── nutrition_db.json          # Food database with nutrition info
├── src/
│   ├── database.py                # Database handler
│   ├── nlp_parser.py              # Gemini AI integration
│   └── nutrition_calculator.py    # Nutrition calculations
├── main.py                        # Main CLI application
├── requirements.txt               # Python dependencies
├── .env                           # API keys (not committed)
└── README.md                      # This file
```

## 🛠️ Adding New Foods

To add new foods to the database, edit `data/nutrition_db.json`:

```json
{
  "id": 16,
  "name": "food_name",
  "aliases": ["alternative_name1", "alternative_name2"],
  "serving_size": "1 serving description",
  "serving_size_grams": 100,
  "calories": 150,
  "protein": 5,
  "carbs": 25,
  "fats": 3,
  "fiber": 2
}
```

## 🐛 Troubleshooting

### "Gemini API key not found"
- Make sure `.env` file exists in the root directory
- Check that `GEMINI_API_KEY` is set correctly
- Verify the API key is valid

### "Database file not found"
- Ensure `data/nutrition_db.json` exists
- Check that you're running from the project root directory

### Import errors
- Make sure `src/__init__.py` exists (can be empty)
- Verify virtual environment is activated
- Run `pip install -r requirements.txt` again

## 🚀 Next Steps (Future Enhancements)

- [ ] Web interface with Streamlit/FastAPI
- [ ] Daily meal tracking and history
- [ ] Visual charts and graphs
- [ ] Meal recommendations based on goals
- [ ] Image recognition for food photos
- [ ] Export reports to PDF/Excel
- [ ] Multi-user support
- [ ] Custom nutrition goals

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to add more foods to the database or suggest improvements!

---

**Made with ❤️ for healthier eating habits**