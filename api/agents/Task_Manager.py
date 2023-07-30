from model import query_model
from utils import read_txt_file_as_string


class Task_Manager:
    def __init__(self, tasks: dict = {}):
        self.tasks = tasks

    def get_task(self, web_voyager):

        if web_voyager.iteration == 0:
            return web_voyager.initial_task

        #OR REPLACE THIS WITH PREDEFINED TASKS
        action_prompt = read_txt_file_as_string("api/prompts/action_template.txt").format(str(web_voyager.tools), str(web_voyager.history))
        response = query_model(action_prompt)
        return response

    def get_task_dict(self):
        return self.tasks
