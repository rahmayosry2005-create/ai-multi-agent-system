from agents.pm_agent import pm_node
from agents.coder_agent import coder_node
from agents.reviewer_agent import reviewer_node

# Create an initial test state
test_state = {
    "task": "Write a Python function to check if a word is a palindrome.",
    "code": "",
    "review_feedback": "",
    "current_iteration": 0,
    "max_iterations": 3,
    "messages": []
}

print("--- Testing PM Agent ---")
pm_result = pm_node(test_state)
test_state.update(pm_result)
print(pm_result)

print("\n--- Testing Coder Agent ---")
coder_result = coder_node(test_state)
test_state.update(coder_result)
print(test_state["code"])

print("\n--- Testing Reviewer Agent ---")
reviewer_result = reviewer_node(test_state)
test_state.update(reviewer_result)
print(test_state["review_feedback"])