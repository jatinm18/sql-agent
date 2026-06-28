# SQL Agent with LangChain + Gemini

A conversational AI agent that answers natural language questions about a SQL database.

## Features
- 🤖 Powered by Google Gemini via LangChain
- 🗄️ Queries a SQLite database (Chinook sample DB)
- ✅ Human-in-the-loop approval before executing SQL
- 🔧 Built with LangGraph for agent orchestration

## Tech Stack
- LangChain
- LangGraph
- Google Gemini (gemini-2.5-flash-lite)
- SQLite

## Setup

1. Clone the repo
```bash
   git clone https://github.com/your-username/sql-agent.git
   cd sql-agent
```

2. Create a virtual environment
```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Add your Google API key to `.env`
