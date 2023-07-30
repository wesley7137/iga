from langchain.tools import Tool

def writeText(text,path="code.py"):
    with open(path, "w") as f:
        f.write(text)

    return path

def get_write_tool():
    return Tool(
        name="writeFile",
        func=writeText,
        description="useful for when you want write code to a file name code.py. Returns the path to the file.",
    )