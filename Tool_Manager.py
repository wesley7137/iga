from claude import query_claude
from utils import read_txt_file_as_string, extract_python_code
import re
class Tool_Manager:
    def __init__(
        self,
        tools: dict={}):

        self.tools = tools

    def get_tools_dict(self):
        return self.tools

    def should_build(self, web_voyager, task):
        should_build_prompt = read_txt_file_as_string("prompts/should_build.txt").format(task, str(self.tools), str(web_voyager.history))
        response = query_claude(should_build_prompt)
        #Add a check so that it is in the right format
        return response

    def build_tool(self, web_voyager, task, should_build):
        build_tool_prompt = read_txt_file_as_string("prompts/build_tool.txt").format(task, str(self.tools), str(web_voyager.history))
        response = query_claude(build_tool_prompt)
        code = extract_python_code(response)
        return code