import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from src.database import NutritionDatabase
from src.nlp_parser import MealParser
from src.nutrition_calculator import NutritionCalculator
from src.chatbot_handler import NutritionChatbot

# Page config
st.set_page_config(
    page_title="🥗 NutriBot - Smart Nutrition Chatbot", 
    page_icon="🥗", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        max-width: 900px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin: 0.75rem 0;
        max-width: 75%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        float: right;
        clear: both;
    }
    
    .bot-message {
        background: #f0f2f6;
        color: #333;
        margin-right: auto;
        float: left;
        clear: both;
    }
    
    .chat-container {
        clear: both;
        overflow: auto;
    }
    
    .nutrition-table {
        margin: 1rem 0;
        clear: both;
    }
    
    .typing-indicator {
        display: inline-block;
        padding: 1rem 1.5rem;
        background: #f0f2f6;
        border-radius: 20px;
        margin: 0.75rem 0;
    }
    
    .typing-indicator span {
        height: 10px;
        width: 10px;
        float: left;
        margin: 0 2px;
        background-color: #667eea;
        display: block;
        border-radius: 50%;
        opacity: 0.4;
        animation: loadingFade 1s infinite;
    }
    
    .typing-indicator span:nth-child(1) {
        animation-delay: 0s;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes loadingFade {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def load_components():
    db = NutritionDatabase()
    parser = MealParser()
    calculator = NutritionCalculator(db)
    chatbot = NutritionChatbot()
    return db, parser, calculator, chatbot

db, parser, calculator, chatbot = load_components()

# SQLite setup
DB_PATH = "meal_history.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meal_type TEXT,
        description TEXT,
        calories REAL,
        protein REAL,
        carbs REAL,
        fats REAL,
        fiber REAL
    )''')
    conn.commit()
    conn.close()

init_db()

def log_meal(date, meal_type, description, nutrition):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO meals (date, meal_type, description, calories, protein, carbs, fats, fiber)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (date, meal_type, description, nutrition['calories'], 
               nutrition['protein'], nutrition['carbs'], nutrition['fats'], nutrition['fiber']))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        'SELECT date as Date, meal_type as "Meal Type", description as Description, '
        'calories as Calories, protein as Protein, carbs as Carbs, fats as Fats, fiber as Fiber '
        'FROM meals ORDER BY date DESC, meal_type',
        conn
    )
    conn.close()
    return df

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'show_history' not in st.session_state:
    st.session_state.show_history = False
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'pending_input' not in st.session_state:
    st.session_state.pending_input = None

# Sidebar
with st.sidebar:
    st.markdown("### 📂 Navigation")
    
    # Navigation buttons
    if st.button("💬 Chat", use_container_width=True, type="primary" if not st.session_state.show_history else "secondary"):
        st.session_state.show_history = False
        st.rerun()
    
    if st.button("📊 History", use_container_width=True, type="primary" if st.session_state.show_history else "secondary"):
        st.session_state.show_history = True
        st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 🎯 Quick Stats")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM meals')
    total_meals = c.fetchone()[0]
    
    c.execute('SELECT SUM(calories) FROM meals WHERE date = ?', 
              (datetime.now().strftime('%Y-%m-%d'),))
    today_calories = c.fetchone()[0] or 0
    conn.close()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Meals", total_meals)
    with col2:
        st.metric("🔥 Today", f"{today_calories:.0f} cal")
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Try Saying:")
    st.info("👋 Hi there!\n\n🍽️ I had 2 chapatis for lunch\n\n❓ What's healthy?\n\n🥗 Give me tips")

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🥗 NutriBot</h1>
    <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>Your Friendly Nutrition Assistant</p>
</div>
""", unsafe_allow_html=True)

# Show History or Chat
if st.session_state.show_history:
    st.markdown("### 📊 Meal History")
    
    df = get_history()
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"meal_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No meals logged yet! Start chatting to track your meals.")

else:
    # Chat Interface
    st.markdown("### 💬 Chat with NutriBot")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-container">
                    <div class="chat-message user-message">
                        <strong>You:</strong> {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-container">
                    <div class="chat-message bot-message">
                        <strong>🥗 NutriBot:</strong> {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # If there's nutrition data, show simple table
            if "nutrition_data" in message:
                result = message["nutrition_data"]
                
                # Create DataFrame for the table
                items_data = []
                for item in result['items']:
                    if item['status'] == 'success':
                        items_data.append({
                            'Food Item': item['food'].title(),
                            'Quantity': f"{item['quantity']} {item['unit']}",
                            'Calories': f"{item['calories']}",
                            'Protein': f"{item['protein']}g",
                            'Carbs': f"{item['carbs']}g",
                            'Fats': f"{item['fats']}g"
                        })
                    else:
                        items_data.append({
                            'Food Item': f"❌ {item['food'].title()}",
                            'Quantity': 'N/A',
                            'Calories': 'Not found',
                            'Protein': '-',
                            'Carbs': '-',
                            'Fats': '-'
                        })
                
                # Add totals row
                totals = result['totals']
                items_data.append({
                    'Food Item': '**TOTAL**',
                    'Quantity': '',
                    'Calories': f"**{totals['calories']:.0f}**",
                    'Protein': f"**{totals['protein']:.1f}g**",
                    'Carbs': f"**{totals['carbs']:.1f}g**",
                    'Fats': f"**{totals['fats']:.1f}g**"
                })
                
                df_items = pd.DataFrame(items_data)
                
                st.markdown('<div class="nutrition-table">', unsafe_allow_html=True)
                st.dataframe(df_items, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Process pending input (if any) - AFTER displaying messages
    if st.session_state.pending_input and not st.session_state.processing:
        st.session_state.processing = True
        user_input = st.session_state.pending_input
        st.session_state.pending_input = None
        
        # Show typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="chat-container">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get bot response
        response = chatbot.chat(user_input, st.session_state.conversation_history)
        typing_placeholder.empty()
        
        if response['type'] == 'meal_analysis':
            # Meal analysis
            meal_description = response.get('meal_description', user_input)
            
            # Add simple response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Sure! Here's your nutrition breakdown:"
            })
            
            # Analyze
            parsed_meal = parser.parse_meal(meal_description)
            
            if 'error' not in parsed_meal:
                result = calculator.calculate_meal(parsed_meal)
                
                # Add table with data
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Your {result['meal_type']} has {result['totals']['calories']:.0f} calories and {result['totals']['protein']:.1f}g protein. Looking good! 💪",
                    "nutrition_data": result
                })
                
                # Log meal
                log_meal(
                    date=datetime.now().strftime('%Y-%m-%d'),
                    meal_type=result['meal_type'],
                    description=meal_description,
                    nutrition=result['totals']
                )
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I couldn't analyze that meal. Could you describe it again? 🤔"
                })
        
        elif response['type'] == 'conversation':
            # Regular chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['message']
            })
        
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, something went wrong. Please try again! 😅"
            })
        
        # Update history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        st.session_state.conversation_history.append({"role": "assistant", "content": response.get('message', '')})
        
        st.session_state.processing = False
        st.rerun()
    
    # Initial greeting if no messages
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="chat-container">
            <div class="chat-message bot-message">
                <strong>🥗 NutriBot:</strong> Hello! 👋 I'm NutriBot, your personal nutrition assistant! 
                Just tell me what you had to eat, and I'll analyze it for you. How can I help you today?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input and not st.session_state.processing:
        # Add user message FIRST (so it shows immediately)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Store input for processing
        st.session_state.pending_input = user_input
        
        # Rerun to show user message immediately
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p style='margin: 0;'>🥗 <strong>NutriBot</strong> - Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)