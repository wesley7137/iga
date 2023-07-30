from model import query_model
from utils import read_txt_file_as_string, extract_python_code, write_tool
import json as JSON

class Tool_Manager:
    def __init__(
        self,
        tools):
        self.tools = tools

        return 

    def should_build(self, web_voyager, task):
        print(task, str(web_voyager.tools), str(web_voyager.history))
        should_build_prompt = read_txt_file_as_string("prompts/should_build.txt").format(task, str(web_voyager.tools))
        response = query_model(should_build_prompt)
        print("response", response)
        #Add a check so that it is in the right format
        response = JSON.loads(response)
        return response

    def build_tool(self, task, should_build):
        build_tool_prompt = read_txt_file_as_string("prompts/build_tool.txt").format(task, should_build['explanation'])
        response = query_model(build_tool_prompt)
        python_file = response.split()[0]
        code = extract_python_code(response)
        python_file = "tools/{}".format(python_file)
        write_tool(python_file, code)
        return python_file

    def code_task(self, web_voyager, task):
        code_task_prompt = read_txt_file_as_string("prompts/build_task.txt").format(task, self.tools)
        response = query_model(code_task_prompt)
        python_file = response.split()[0]
        code = extract_python_code(response)
        python_file = "tasks/{}".format(python_file)
        return python_file

    def get_tool(self, task):
        code_task_prompt = read_txt_file_as_string("prompts/pick_skill_template.txt").format(task, self.tools)
        response = query_model(code_task_prompt)
        return response

