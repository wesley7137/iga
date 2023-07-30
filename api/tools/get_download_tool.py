import subprocess
import sys
from langchain.tools import Tool
from langchain.document_loaders import PyPDFLoader
import wget

def download_file(url) -> str:
    """
    Install dependencies and run code
    Args:
    url (str): url to download file from
    Returns:
    result --> output results
    """
    try:
        # Install required dependencies
        return wget.download(url)
    except Exception as e:
        print(f"An error occurred: {e}")
    

def get_download_file_tool():
    Tool(
        name="downloadFile",
        func=wget.download,
        description="useful for when you need to download a file from a url",
    )


