from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent
from typing import List, Tuple, Any, Union
from langchain.schema import AgentAction, AgentFinish


class AnthropicAgent(BaseSingleActionAgent):
    
    tools: List[Tool]
    chain: Any

    @property
    def input_keys(self):
        return ["input"]

    def plan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        log = ""
        for action, observation in intermediate_steps:
            log += f"<tool>{action.tool}</tool><tool_input>{action.tool_input}</tool_input><observation>{observation}</observation>"
        tools = ""
        for tool in self.tools:
            tools += f"{tool.name}: {tool.description}\n"
        response = self.chain.invoke({"intermediate_steps": log, "tools": tools, "question": kwargs["input"]})
        if "</tool>" in response.content:
            t, ti = response.content.split("</tool>")
            _t = t.split("<tool>")[1]
            _ti = ti.split("<tool_input>")[1]
            return AgentAction(tool=_t, tool_input=_ti, log=response.content)
        elif "<final_answer>" in response.content:
            t, ti = response.content.split("<final_answer>")
            return AgentFinish(return_values={"output": ti}, log=response.content)
        else:
            raise ValueError

    async def aplan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        raise ValueError