from langchain_core.messages import SystemMessage, HumanMessage
from agents.agents import reviewer_model  # Import the OpenRouter reviewer model

def reviewer_node(state):
    """
    Reviewer Agent: Reviews the generated code for bugs, logic errors, and best practices.
    """
    task = state["task"]
    current_code = state.get("code", "")
    
    # 1. Define the system prompt for the Reviewer role (cognitive diversity via OpenRouter)
    system_prompt = SystemMessage(content=(
        "You are a strict, detail-oriented Senior Code Reviewer. "
        "Analyze the provided Python code for bugs, edge cases, performance issues, and adherence to best practices. "
        "If the code is correct and fulfills the task, explicitly state 'APPROVED'. "
        "Otherwise, provide constructive and clear feedback for improvement."
    ))
    
    # 2. Build the human prompt containing the task and code to review
    human_prompt = HumanMessage(content=f"""
    Task to check: {task}
    
    Code to Review:
    {current_code}
    
    Provide your review feedback and decision.
    """)
    
    # 3. Invoke the OpenRouter model
    response = reviewer_model.invoke([system_prompt, human_prompt])
    feedback = response.content
    
    print(f"\n[Reviewer Agent] Code reviewed successfully.")
    
    return {
        "review_feedback": feedback,
        "messages": [f"Reviewer: Code review completed."]
    }