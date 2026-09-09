from langgraph.graph import StateGraph, END
from state import AgentState
from agents.pm_agent import pm_node
from agents.coder_agent import coder_node
from agents.reviewer_agent import reviewer_node

# Import guardrails
from guardrails.input_guard import validate_input
from guardrails.output_guard import validate_output

# Initialize the workflow graph
workflow = StateGraph(AgentState)

# Add agent nodes
workflow.add_node("pm_node", pm_node)
workflow.add_node("coder_node", coder_node)
workflow.add_node("reviewer_node", reviewer_node)

# Define workflow sequence
workflow.set_entry_point("pm_node")
workflow.add_edge("pm_node", "coder_node")
workflow.add_edge("coder_node", "reviewer_node")

def should_continue(state: AgentState):
    """
    Checks if code is approved or max iterations reached.
    """
    feedback = state.get("review_feedback", "")
    iteration = state.get("current_iteration", 0)
    max_iters = state.get("max_iterations", 3)
    
    if "APPROVED" in feedback or iteration >= max_iters:
        return "end"
    return "continue"

workflow.add_conditional_edges(
    "reviewer_node",
    should_continue,
    {
        "continue": "pm_node",
        "end": END
    }
)

app = workflow.compile()

if __name__ == "__main__":
    print("--- Starting AI Multi-Agent Coding System ---\n")
    
    # 1. Get user prompt/task
    user_task = "Write a Python function to check if a word is a palindrome."
    print(f"User Prompt: {user_task}\n")
    
    # 2. Run Input Guardrail
    is_safe, input_msg = validate_input(user_task)
    if not is_safe:
        print(f"[Input Guardrail Blocked]: {input_msg}")
        exit(1)
    print("[Input Guardrail Passed]: Request is safe and valid.\n")
    
    # 3. Initialize Graph State
    initial_state = {
        "task": user_task,
        "code": "",
        "review_feedback": "",
        "current_iteration": 0,
        "max_iterations": 3,
        "messages": []
    }
    
    # 4. Invoke Workflow
    final_state = app.invoke(initial_state)
    
    print("\n--- Workflow Execution Completed ---\n")
    final_code = final_state.get("code", "")
    final_feedback = final_state.get("review_feedback", "")
    
    # 5. Run Output Guardrail
    is_valid_out, output_msg = validate_output(final_code)
    if not is_valid_out:
        print(f"[Output Guardrail Warning]: {output_msg}")
    else:
        print("[Output Guardrail Passed]: Final code structure and syntax are valid.\n")
    
    print("Final Generated Code:\n")
    print(final_code)
    print("\nFinal Review Feedback:\n")
    print(final_feedback)

    # Clean up final_code if it's extracted from a structured list/dict response
    if isinstance(final_code, list) and len(final_code) > 0:
        if isinstance(final_code[0], dict) and "text" in final_code[0]:
            final_code = final_code[0]["text"]