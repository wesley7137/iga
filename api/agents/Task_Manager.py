from claude import query_claude
from utils import read_txt_file_as_string


class Task_Manager:
    def __init__(self, tasks: dict = {}):
        self.tasks = tasks

    def get_task(self, web_voyager):
        # OR REPLACE THIS WITH PREDEFINED TASKS
        action_prompt = read_txt_file_as_string("prompts/action_template.txt").format(
            str(web_voyager.tools), str(web_voyager.history)
        )
        response = query_claude(action_prompt)
        return response

    def get_task_dict(self):
        return self.tasks
