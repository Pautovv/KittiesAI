import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "MAS_Syndicate_v1")

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0, 
    api_key=os.getenv("GROQ_API")
)