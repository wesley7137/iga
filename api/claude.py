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
from AnthropicAgent import AnthropicAgent
from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent

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


def query_claude(request,tools=tool_list) -> str:
    agent_instructions = """You are a helpful assistant. Help the user answer any questions.

    You have access to the following tools:

    {tools}

    In order to use a tool, you can use <tool></tool> and <tool_input></tool_input> tags. \
    You will then get back a response in the form <observation></observation>
    For example, if you have a tool called 'search' that could run a google search, in order to search for the weather in SF you would respond:

    <tool>search</tool><tool_input>weather in SF</tool_input>
    <observation>64 degrees</observation>

    When you are done, respond with a final answer between <final_answer></final_answer>. For example:

    <final_answer>The weather in SF is 64 degrees</final_answer>

    Begin!

    Question: {question}"""
    model = ChatAnthropic(model="claude-2")
    prompt_template = ChatPromptTemplate.from_template(agent_instructions) + AIMessagePromptTemplate.from_template("{intermediate_steps}")
    chain = prompt_template | model.bind(stop=["</tool_input>", "</final_answer>"])
    
    agent = AnthropicAgent(tools=tool_list, chain=chain)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
       
    for step in agent_executor.iter(request):
        print(step)
        if output := step.get("intermediate_step"):
            action, value = output[0]

    return value
