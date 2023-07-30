from environment.Web_Voyager_Env import Env
from agents.Tool_Manager import Tool_Manager
from agents.Critic import Critic
from agents.Task_Manager import Task_Manager
from typing import Optional
from environment.manage_skills import initialize_skills
import json

from dotenv import load_dotenv

load_dotenv() # This will load all the environment variables from a .env file located in the same directory as the script


class Web_Voyager:
    def __init__(
        self,
        initial_task: Optional[str] = None,
        initial_tools: dict = {},
        task_model_name: str = "claude2",
        task_llm_key: str = None,
        tool_model_name: str = "gpt4",
        tool_llm_key: str = None,
        max_iterations: int = 50,
        tool_library_dir: str = "./tools",
        history: dict = {},
        tools: dict = {},
        iteration: int = 0,
        tool_build_attempts: int = 5,
        done: bool = False,
    ):
        self.initial_task = initial_task
        self.env = Env()
        self.tool_manager = Tool_Manager(tools)
        self.critic = Critic()
        self.task_manager = Task_Manager()
        self.task_model_name = task_model_name
        self.task_llm_key = task_llm_key
        self.tool_model_name = tool_model_name
        self.tool_llm_key = tool_llm_key
        self.max_iterations = max_iterations
        self.tool_library_dir = tool_library_dir
        self.history = history
        self.tools = tools
        self.iteration = iteration
        self.tool_build_attempts = tool_build_attempts
        self.done = done
        self.stop_flag = False

    def should_stop(self):
        return self.stop_flag

    def stop(self):
        self.stop_flag = True

    def increment_iter(self):
        self.iteration += 1

    def step(self):
        if self.should_stop():
            # Logic to clean up or finalize any tasks before stopping
            return

        if self.iteration > self.max_iterations:
            raise ValueError("Agent has exceeded maximum iterations tool building")
        task = self.task_manager.get_task(self)
        for i in range(self.tool_build_attempts):
            print("new attempt")
            #print('skills', self.tools)
            shouldnt_build = self.tool_manager.should_build(self, task)
            if shouldnt_build["result"] == 'success':
                #get llm to pick the best tool to use for the task
                tool_lst = self.tool_manager.get_tool(task)
                print(tool_lst)
                tool_lst = json.loads(tool_lst)
                print(tool_lst)
                action_file = tool_lst[0]
                parameters = tool_lst[1]
                #execute the task
                result = self.env.execute_action(action_file, parameters)
                break
            elif shouldnt_build["result"] == 'failure':
                tool_file = self.tool_manager.build_tool(task, shouldnt_build)
                #NEED TO CHECK IF SKILL BUILT WORKS. MAYBE ASK CLAUDE TO WRITE A TEST CASE
                tool_eval = self.critic.evaluate_tool(tool_file)
                tool_lst =self.tool_manager.get_tool(task)
                tool_lst = json.loads(tool_lst)

                print(tool_lst)
                action_file = tool_lst[0]
                parameters = tool_lst[1]
                result = self.env.execute_action(action_file, parameters)

            #code_eval = self.critic.evaluate_task(task, self.env)

            #if code_eval['result']=='success':
            #     break
            #else:
                #update the skill dict
                #evalute the py file, error, and changes in state to refine the task, 
            # self.history[task['name']]={code_eval['result']: code}
            # Can incorporate human feedback here            



            else:
                raise ValueError("should_build result not recognized")

if __name__ == "__main__":
    skills = initialize_skills()
    
    initial_task = "please use the search tool to get me a url for an arxiv paper about string theory"
    web_voyager = Web_Voyager(
        initial_task=initial_task, 
        tools=skills)
    #while web_voyager.iteration < web_voyager.max_iterations and not web_voyager.done:
    web_voyager.step()
    #web_voyager.increment_iter()
