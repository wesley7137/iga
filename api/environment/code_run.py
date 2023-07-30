import subprocess
import sys
# from langchain.tools import Tool

dependencies = [
    "pydantic",
    "langchain",
    "flask",
    "python-dotenv",
    "torch",
    "numpy",
]  # add all dependenceis


def run_code_with_pip_dependencies(code, dependencies=dependencies):
    """
    Install dependencies and run code
    Args:
    dependencies (list): List of packages to install
    code (str): Python code to run
    """
    try:
        # Install required dependencies
        for dep in dependencies:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

        # Execute the provided code
        exec(code)
    except Exception as e:
        print(f"An error occurred: {e}")




# def get_code_tool():
#     return Tool(
#         name="code",
#         func=lambda x: run_code_with_pip_dependencies(dependencies, x),
#         description="useful for when you need to run code",
#     )
