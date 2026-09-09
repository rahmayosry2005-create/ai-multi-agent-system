# 🤖 Multi-Agent Software Development Team

Transforming single-line natural language prompts into production-grade Python code through collaborative AI agents, powered by LangGraph, LlamaIndex, and Streamlit.

---

## 🚀 Overview
This project simulates an automated software development lifecycle using a multi-agent architecture. Instead of relying on a single prompt-response loop, the system divides the workload among specialized AI agents that collaborate, execute code, validate syntax using Abstract Syntax Trees (AST), and self-correct iteratively.

## 👥 Team Architecture
- **PM Agent (Product Manager):** Analyzes the user prompt, defines structural requirements, and sets acceptance criteria.
- **Coder Agent:** Writes and executes Python code leveraging retrieval-augmented generation and execution tools.
- **Reviewer Agent:** Validates the generated code, checks for security and performance issues, and provides constructive feedback for iterative refinement.

## 🛡️ Guardrails & Safety
- **Input Guardrail:** Intercepts and blocks prompt injections or malicious tasks before processing.
- **Output Guardrail:** Validates generated code syntax using AST parsing to ensure safety and prevent runtime crashes.

## 💻 Tech Stack
- **Orchestration:** LangGraph
- **Frontend & UI:** Streamlit (with a custom, responsive Dark Mode)
- **Data & Tools:** LlamaIndex, Python AST Module
- **LLM Integration:** Google Gemini API

## ⚙️ Local Installation & Setup

1. **Clone the repository:**
   git clone https://github.com/rahmayosry2005-create/ai-multi-agent-system.git
   cd ai-multi-agent-system

2. **Install dependencies:**
   pip install -r requirements.txt

3. **Set up environment variables:**
   Create a .env file in the root directory and add your API key:
   GOOGLE_API_KEY="your_api_key_here"

4. **Run the Streamlit application:**
   streamlit run app.py
   