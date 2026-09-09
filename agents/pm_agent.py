from langchain_core.messages import SystemMessage, HumanMessage
from agents.agents import gemini_model  
def pm_node(state):
    """
    Project Manager Agent: Oversees the project, evaluates progress, and manages workflow state.
    """
    task = state["task"]
    current_iter = state["current_iteration"]
    max_iter = state["max_iterations"]
    
    # 1. Define the system prompt for the PM role
    system_prompt = SystemMessage(content=(
        "You are an expert Agile Project Manager. "
        "Your job is to oversee software development tasks, track iterations, "
        "and keep track of the overall project progress."
    ))
    
    # 2. Build the human prompt with current state metrics
    human_prompt = HumanMessage(content=f"""
    Task: {task}
    Current Iteration: {current_iter + 1}
    Max Allowed Iterations: {max_iter}
    
    Acknowledge the current status and coordinate the next step.
    """)
    
    # 3. Invoke the model
    response = gemini_model.invoke([system_prompt, human_prompt])
    
    print(f"\n[PM Agent] Managing task (Iteration {current_iter + 1}/{max_iter})")
    
    return {
        "current_iteration": current_iter + 1,
        "messages": [f"PM: Managing iteration {current_iter + 1} for task -> {task}"]
    }