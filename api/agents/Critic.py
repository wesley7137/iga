from model import query_model
from utils import read_txt_file_as_string


class Critic:
    def __init__(self):
        pass

    def evaluate_tool(self,python_file):
        #For now just ask claude if the code is good
        query = "Does this code work as intended. Answer with only yes or no. (one word): {}".format(read_txt_file_as_string(python_file))
        response = query_model(query)
        return response.split()[0]

    def evaluate_task(self,web_voyager, task):
        prev = web_voyager.env.get_previous_state()
        curr = web_voyager.env.get_previous_state()
        critc_prompt = read_txt_file_as_string("api/prompts/critic.txt").format(task, str(prev), str(curr))
        response = query_model(critc_prompt)
        return response
