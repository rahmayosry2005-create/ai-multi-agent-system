import os
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini

def init_knowledge_base():
    """
    Initializes a local LlamaIndex Knowledge Base with Python best practices 
    and design patterns to assist the Coder agent.
    """
    # Sample documents containing coding best practices and design principles
    documents_content = [
        "Python Best Practices: Always use type hinting for function arguments and return types to improve code readability and maintainability.",
        "Error Handling: Use specific exception handling (e.g., ValueError, TypeError) instead of a broad bare 'except:' clause.",
        "Clean Code: Keep functions small, focused on a single responsibility, and provide comprehensive docstrings with examples.",
        "Object-Oriented Programming: Favor encapsulation and composition over deep inheritance hierarchies. Ensure proper use of dunder methods."
    ]
    
    docs = [Document(text=content) for content in documents_content]
    
    # Setup lightweight local embeddings to avoid heavy API overhead for local search
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # Create the vector index from documents
    index = VectorStoreIndex.from_documents(docs)
    return index

def query_knowledge_base(query_text: str) -> str:
    """
    Queries the knowledge base to retrieve relevant coding best practices.
    """
    try:
        index = init_knowledge_base()
        query_engine = index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)
    except Exception as e:
        return f"Could not retrieve knowledge base info: {str(e)}"