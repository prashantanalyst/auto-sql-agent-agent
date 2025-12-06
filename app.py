import streamlit as st
import sqlite3
import random
from datetime import datetime, timedelta
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Prashant's AI Analyst", page_icon="🚀", layout="wide")

# --- 2. SELF-HEALING DATA GENERATOR ---
def ensure_database_exists():
    # This function creates the database automatically if it's missing
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='sales'")
    if c.fetchone()[0] == 0:
        with st.spinner('⚠️ Database empty. Generating data...'):
            c.execute('''CREATE TABLE IF NOT EXISTS products
                         (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)''')
            c.execute('''CREATE TABLE IF NOT EXISTS sales
                         (sale_id INTEGER PRIMARY KEY, product_id INTEGER, 
                          date TEXT, quantity INTEGER, total_amount REAL)''')
            
            # Fake Data
            products = [('Laptop', 'Electronics', 1200), ('Smartphone', 'Electronics', 800), 
                        ('Table', 'Home', 150), ('Chair', 'Home', 80), ('Headphones', 'Electronics', 200)]
            c.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products)
            
            for i in range(100):
                p_id = random.randint(1, len(products))
                price = c.execute("SELECT price FROM products WHERE product_id = ?", (p_id,)).fetchone()[0]
                qty = random.randint(1, 5)
                date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
                c.execute("INSERT INTO sales (product_id, date, quantity, total_amount) VALUES (?, ?, ?, ?)", 
                          (p_id, date, qty, price * qty))
            conn.commit()
            st.success("✅ Database generated successfully!")
    conn.close()

# Run the check
ensure_database_exists()

# --- 3. SIDEBAR (YOUR BRANDING) ---
st.sidebar.markdown("## ⚙️ Settings")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Built by Prashant Yadav")
st.sidebar.info("Architecture: LangChain + Llama 3 + Streamlit")

if not api_key:
    st.title("🚀 Auto-SQL: Autonomous Data Agent")
    st.warning("⬅️ Please enter your API Key in the sidebar to start.")
    st.stop()

# --- 4. CONNECT TO AI BRAIN ---
try:
    db = SQLDatabase.from_uri("sqlite:///sales.db")
    llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- 5. CHAT INTERFACE ---
st.title("🚀 Auto-SQL: Autonomous Data Agent")
st.caption("I can analyze your sales database. Try asking: 'What is the total revenue?'")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello Prashant! I am ready to query your database."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        try:
            response = agent_executor.invoke(prompt)
            st.write(response["output"])
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        except Exception as e:
            st.error(f"Error: {e}")
