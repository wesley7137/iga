# from langchain.tools import BaseTool, StructuredTool, Tool, tool
# from langchain.utilities import GoogleSerperAPIWrapper


# def get_search_tool():
#     search = GoogleSerperAPIWrapper()

<<<<<<< HEAD
#     return Tool(
#         name="search",
#         func=lambda x : search.run(x),
#         description="useful for when you need to ask with search (especially for a research paper)",
#     )
        
=======
    return Tool(
        name="search",
        func=lambda x: search.run(x),
        description="useful for when you need to ask with search (especially for a research paper)",
    )
>>>>>>> 76d6f63d09fb6d0378a2808cf1bca3da2692a97d
