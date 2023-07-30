import subprocess
import sys
from langchain.tools import Tool
from langchain.document_loaders import PyPDFLoader

def get_read_pdf_tool():
    return Tool(
        name="readPDF",
        func=lambda x: PyPDFLoader(x).load_and_split()[0:3],
        description="useful for when you want to read a pdf file. Returns the first three pages.",
    )
