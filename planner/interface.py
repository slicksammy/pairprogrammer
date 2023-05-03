import functools
import re
from completions.interface import Interface as CompletionsInterface

class Interface:
    def __init__(self):
        self.messages = []
        self.tasks = []
        self.requirements = """
        I need to build a ruby cli to communicate with my server. The cli should be used as pairprogammer COMMAND ARGUMENTS. I need this cli to be extendable.
        Currently the usages I have are pairprogrammer respond MESSAGE, pairprogrammer tasks, pairprogrammer messages, pairprogrammer help.
        """

        prompt = self.build_prompt()
        self.append_message(prompt, role="system")

    def generate_task_list(self):
        content = f"""
        Generate a list of tasks to complete the requirement in the following format:
        TASK: ...
        TASK: ...
        ...
        """
        self.append_message(content, role="user")
        response = self.run_completion()

        self.tasks = re.findall(r"TASK: (.+)", response)

    @functools.cache
    def system_message(self):
        return { "role": "system", "content": self.build_prompt() }
    
    def build_prompt(self):
        return self.base_prompt().replace("<<REQUIREMENTS>>", self.requirements)
    
    def append_message(self, content, role="user"):
        self.messages.append({ "content": content, "role": role })

    def run_completion(self, model="gpt-4"):
        completions_interface = CompletionsInterface()
        if completions_interface.available_completion_tokens(self.messages, model) > 200:
            content = completions_interface.run_completion(self.messages, model)
            self.append_message(content, role="assistant")
            return content
        else:
            raise Exception("not enough tokens")

    def base_prompt(self):
        return f"""
        You are given a requirement and need to plan out tasks to complete it. You are to converse with the user until you have a clear understanding of what needs to get done.

        In addition to the requirements, you should figure out:
        - What files need to be created or modified
        - If there are any examples of the code you need to write
        - If there are any additional dependencies that need to be installed

        REQUIREMENTS:
        <<REQUIREMENTS>>

        STRING
        """