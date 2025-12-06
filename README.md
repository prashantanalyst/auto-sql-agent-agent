# 🚀 Auto-SQL: Autonomous Enterprise Data Agent

### 🤖 Overview
Auto-SQL is an intelligent agentic workflow designed to democratize data access. It allows non-technical stakeholders to query complex databases using natural language, eliminating the need for manual SQL writing.

**Built with:** Python, LangChain, Groq (Llama 3), Streamlit.

### ✨ Key Features
- **Natural Language to SQL:** Translates questions like *"What is the total revenue for Electronics?"* into executable SQL queries.
- **Self-Healing Architecture:** The system automatically checks if the database exists; if not, it generates a synthetic dataset (`sales.db`) on the fly.
- **Autonomous Error Correction:** If the LLM generates invalid SQL, the agent captures the error, reads the schema, and self-corrects the query without human intervention.
- **Enterprise-Grade Model:** Powered by Meta's **Llama 3.3 (70B)** via Groq for sub-second inference speeds.

### 🛠️ Architecture
1. **User Interface:** Streamlit (Chat-based).
2. **Brain:** Llama 3.3-70b-versatile (via Groq API).
3. **Orchestrator:** LangChain `SQLDatabaseToolkit`.
4. **Database:** SQLite (local).

### 🚀 How to Run Locally
1. **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/auto-sql-agent.git](https://github.com/your-username/auto-sql-agent.git)
    ```
2. **Install dependencies:**
    ```bash
    pip install streamlit langchain-community langchain-groq
    ```
3. **Run the app:**
    ```bash
    streamlit run app.py
    ```
4. **Enter API Key:**
    - Get a free API Key from [Groq Console](https://console.groq.com).
    - Enter it in the sidebar to activate the agent.

### 👨‍💻 Author
**Prashant Yadav**
*AI Trainer Specialist & Data Analyst*
