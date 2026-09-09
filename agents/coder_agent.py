from langchain_core.messages import SystemMessage, HumanMessage
from agents.agents import gemini_model 
def coder_node(state):
    """
    Coder Agent: Writes or updates Python code based on the task and review feedback.
    """
    task = state["task"]
    feedback = state.get("review_feedback", "")
    current_code = state.get("code", "")
    
    # 1. Define the system prompt defining the agent's role
    system_prompt = SystemMessage(content=(
        "You are an expert Python software engineer. "
        "Write clean, efficient, and well-documented Python code based on the given task. "
        "If there is review feedback from a previous iteration, you MUST fix the issues mentioned."
    ))
    
    # 2. Build the human prompt containing the task and context
    human_prompt = HumanMessage(content=f"""
    Task: {task}
    
    Previous Code:
    {current_code if current_code else "None (Write initial code)"}
    
    Review Feedback to address:
    {feedback if feedback else "None yet."}
    
    Provide ONLY the Python code block as your output.
    """)
    
    # 3. Invoke the model
    response = gemini_model.invoke([system_prompt, human_prompt])
    generated_code = response.content
    
    print(f"\n[Coder Agent] Code generated/updated successfully.")
    
    return {
        "code": generated_code,
        "messages": [f"Coder: Code generated for task -> {task}"]
    }