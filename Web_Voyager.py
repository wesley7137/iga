from Web_Voyager_Env import Web_Voyager_Env
from Skill_Manager import Skill_Manager
from Critic import Critic
from Task_Manager import Task_Manager
class Web_Voyager:
    def __init__(
        self,
        task_model_name: str = "claude2",
        task_llm_key: str = None,
        skill_model_name: str = "gpt4",
        skill_llm_key: str = None,
        max_iterations: int = 50,
        skill_library_dir: str = './skills',
        history: dict = {},
        skills: dict = {},
        iteration: int = 0,
        skill_build_attempts: int = 5
    ):
        self.env = Web_Voyager_Env()
        self.skill_builder = Skill_Manager()
        self.critic = Critic()
        self.task_manager = Task_Manager()
        self.task_model_name = task_model_name
        self.task_llm_key = task_llm_key
        self.skill_model_name = skill_model_name
        self.skill_llm_key = skill_llm_key
        self.max_iterations = max_iterations
        self.skill_library_dir = skill_library_dir
        self.history = history
        self.skills = skills
        self.iteration = iteration
        self.skill_build_attempts = skill_build_attempts

        def increment_iter(self):
            self.iteration += 1

        def step(self):
            if self.iteration > max_iterations:
                raise ValueError("Agent has exceeded maximum iterations skill building")
            task = self.task_manager.get_task(self.history, self.skills)
            for i in range(self.skill_build_attempts):
                code = self.skill_manager.build_skill(task, self.skills, self.history)
                result = self.critic.evaluate_skill(code, self.env)
                if result['result']=='success':
                    break










        


