import re
def read_txt_file_as_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def extract_python_code(response_string):
    pattern = r"```python(.*?)```"  # Regular expression to match Python code block between triple backticks
    match = re.search(pattern, response_string, re.DOTALL)
    if match:
        python_code = match.group(1).strip()
        return python_code
    else:
        print("No Python code block found in the response.")
        return None

def write_tool(script_path, code):
    try:
        with open(script_path, 'w') as file:
            file.write(code)
        print(f"Python script '{script_path}' has been created successfully.")
    except Exception as e:
        print(f"Error creating Python script: {e}")