from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.utilities import GoogleSerperAPIWrapper


def get_search_tool():
    search = GoogleSerperAPIWrapper()
    
    return Tool(
        name="search",
        func=search.run,
        description="useful for when you need to ask with search (especially for a research paper)",
    )
        