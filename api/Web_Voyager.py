from environment.Web_Voyager_Env import Env
from agents.Tool_Manager import Tool_Manager
from agents.Critic import Critic
from agents.Task_Manager import Task_Manager
from typing import Optional

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
        self.tool_manager = Tool_Manager()
        self.critic = Critic()
        self.task_manager = Task_Manager()
        self.task_model_name = task_model_name
        self.task_llm_key = task_llm_key
        self.tool_model_name = tool_model_name
        self.tool_llm_key = tool_llm_key
        self.max_iterations = max_iterations
        self.tool_library_dir = tool_library_dir
        self.history = history
        self.tools = tools | initial_tools
        self.iteration = iteration
        self.tool_build_attempts = tool_build_attempts
        self.done = done

    def increment_iter(self):
        self.iteration += 1

    def step(self):
        if self.iteration > self.max_iterations:
            raise ValueError("Agent has exceeded maximum iterations tool building")
        task = self.task_manager.get_task(self)
        for i in range(self.tool_build_attempts):
            print('skills', self.tools)
            shouldnt_build = self.tool_manager.should_build(self, task)
            print('should_build', shouldnt_build)
            if shouldnt_build["result"] == 'success':
                #get llm to pick the best tool to use for the task

                #execute the task
                result = self.env.execute_action(shouldnt_build['tool'])
                
            elif shouldnt_build["result"] == 'failure':
                return 
            else:
                raise ValueError("should_build result not recognized")
            #     tool_file = self.tool_manager.build_tool(self, task, should_build)
            #     tool_eval = self.critic.evaluate_tool(self, tool_file)
            # code = self.tool_manager.code_task(self, task)
            # code_eval = self.critic.evaluate_task(self, code)
            # if code_eval['result']=='success':
            #     break
            # self.history[task['name']]={code_eval['result']: code}
            # Can incorporate human feedback here

if __name__ == "__main__":
    initial_task = "Find me some bagels online"
    web_voyager = Web_Voyager(
        initial_task=initial_task, 
        initial_tools={
            'useSelenium': { 'file': 'useSelenium.py', 'desc': 'Use Selenium to programmatically interact with a web browser'}, 
            'useBeautifulSoup':{ 'file': 'useBeautifulSoup.py', 'desc': 'Use BeautifulSoup to scrape web content'},
        })
    while web_voyager.iteration < web_voyager.max_iterations and not web_voyager.done:
        web_voyager.step()
        web_voyager.increment_iter()
