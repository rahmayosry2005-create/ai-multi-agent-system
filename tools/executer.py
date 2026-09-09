import subprocess
import sys
import tempfile
import os

def execute_python_code(code_string: str, timeout: int = 5) -> dict:
    """
    Executes a given Python code string in a safe subprocess 
    and returns the execution output, errors, and success status.
    """
    # Clean up markdown code blocks if passed directly
    if "```python" in code_string:
        code_string = code_string.split("```python")[1].split("```")[0].strip()
    elif "```" in code_string:
        code_string = code_string.split("```")[1].split("```")[0].strip()

    # Create a temporary file to run the code
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(code_string)
        temp_file_path = temp_file.name

    try:
        # Run the script using the current python interpreter
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        success = result.returncode == 0
        output = result.stdout if success else result.stderr
        
        return {
            "success": success,
            "output": output.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "Error: Code execution timed out."
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"Error executing code: {str(e)}"
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)