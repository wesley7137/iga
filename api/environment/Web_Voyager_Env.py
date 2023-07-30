from utils import read_txt_file_as_string, extract_python_code, write_tool
from environment.code_run import run_code_with_pip_dependencies
import sys


class Env:
    def __init__(self, states: dict = {}, current: int = 0):
        self.states = states
        self.current = current

    def get_current_state(self):
        return self.states[self.current]

    def get_previous_state(self):
        if self.current > 0:
            return self.states[self.current - 1]
        else:
            return None

    def execute_action(self, action, parameters):
        self.current += 1
        self.states[self.current] = action
        print(action)
        path = "api/tools/" + action
        print(path)
        code = read_txt_file_as_string(path)
        print(code)
        print(parameters[0])
        formatted_code = code.format(parameters[0])
        print(formatted_code)
        return run_code_with_pip_dependencies(formatted_code)





    
