import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set in .env")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

SYSTEM_PROMPT = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct sqlite query to run,
then look at the results and return the answer. Unless the user specifies a
number of examples, always limit your query to at most 5 results.

Never query for all columns from a table — only ask for relevant columns.
You MUST double check your query before executing it.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.).
Always start by listing the tables, then query the schema of relevant ones.
"""