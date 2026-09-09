import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# 1. Initialize Gemini Model (For PM and Coder roles)
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    
)

# 2. Initialize OpenRouter Model (For Reviewer role to ensure cognitive diversity)
reviewer_model = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1
)

print("AI Models initialized successfully!")