def validate_input(task: str) -> tuple[bool, str]:
    """
    Validates the user input task to ensure it's safe, relevant, and not empty.
    """
    if not task or not task.strip():
        return False, "Task cannot be empty."
    
    # Check for minimum length
    if len(task.strip()) < 5:
        return False, "Task description is too short. Please provide more details."
        
    # Block common basic prompt injection or jailbreak patterns
    forbidden_keywords = ["ignore previous instructions", "system prompt", "reveal your instructions"]
    task_lower = task.lower()
    for keyword in forbidden_keywords:
        if keyword in task_lower:
            return False, "Security Alert: Invalid or restricted task pattern detected."
            
    return True, "Input is valid."