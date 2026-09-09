import ast
import re

def validate_output(output_text) -> tuple[bool, str]:
    """
    Validates the generated code or response from the agents 
    to ensure quality, safety, and correct Python syntax.
    """
    # If output_text is passed as a list or dict (e.g., LangChain messages/content), convert to string safely
    if isinstance(output_text, list):
        output_text = "".join(str(item) for item in output_text)
    elif not isinstance(output_text, str):
        output_text = str(output_text)

    if not output_text or not output_text.strip():
        return False, "Output generation failed: Empty response."
    
    if len(output_text.strip()) < 10:
        return False, "Output is too short to be a valid solution."
        
    # Extract Python code blocks if present
    code_match = re.findall(r"```python\n(.*?)\n```", output_text, re.DOTALL)
    
    if code_match:
        code_to_check = code_match[0]
        try:
            ast.parse(code_to_check)
        except SyntaxError as e:
            return False, f"Syntax Error detected in generated code: {e}"
            
    return True, "Output is valid."