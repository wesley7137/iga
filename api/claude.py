from flask import Flask, jsonify, request
from dotenv import load_dotenv
from langchain.chat_models import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.document_loaders import PyPDFLoader
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
import wget

load_dotenv()


def writeText(text, path="code.py"):
    with open(path, "w") as f:
        f.write(text)

    return path


# query_template = ChatPromptTemplate()
search = GoogleSerperAPIWrapper()

tool_list = [
    Tool(
        name="search",
        func=search.run,
        description="useful for when you need to ask with search (especially for a research paper)",
    ),
    Tool(
        name="readFile",
        func=ReadFileTool().run,
        description="useful for when you need to read a file",
    ),
    Tool(
        name="downloadFile",
        func=wget.download,
        description="useful for when you need to download a file from a url",
    ),
    Tool(
        name="readPDF",
        func=lambda x: PyPDFLoader(x).load_and_split()[0:3],
        description="useful for when you want to read a pdf file. Returns the first three pages.",
    ),
    Tool(
        name="writeFile",
        func=writeText,
        description="useful for when you want write code to a file name code.py. Returns the path to the file.",
    ),
    Tool(
        name="createTool",
        func=lambda x: x,
        description="useful for when you to create a new tool. input is a json with name, func, and description. The func argument must be a lambda function Returns the path to the file.",
    ),
    # ReadPDFTool
]


def query_claude(request) -> str:
    llm = ChatAnthropic(model="claude-2", max_tokens_to_sample=2000)
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]

    self_ask_with_search = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
    )
    response = self_ask_with_search.run(request)
    return response
