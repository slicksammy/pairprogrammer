import os
from .parsers.interface import Interface as ParserInterface
from .tasks.interface import Interface as TaskInterface
from ..models import ParsedResponse

class Interface:
    VERSION_CONFIGURATION = {
        "1": {
            "prompt": "v2.txt",
            "parser": "json",
            "tasks": "newline"
        }
    }

    def __init__(self, version, coder):
        self.coder = coder
        self.prompt_version = Interface.VERSION_CONFIGURATION[version]["prompt"]
        self.parser_version = Interface.VERSION_CONFIGURATION[version]["parser"]
        self.tasks_version = Interface.VERSION_CONFIGURATION[version]["tasks"]

    def prompt(self, context, requirements, tasks):
        base_prompt_file = self.__prompt_file()
        prompt = None
        with open(base_prompt_file, 'r') as file:
            prompt = file.read()
        tasks = TaskInterface(self.tasks_version).prompt(tasks)
        response_prompt = ParserInterface(self.parser_version).prompt()
        prompt = prompt.replace("<<CONTEXT>>", context).replace("<<REQUIREMENTS>>", requirements).replace("<<RESPONSE_PROMPT>>", response_prompt).replace("<<TASKS>>", tasks)
        return prompt
        
        
    def parse_response(self, response):
        try:
            parsed = ParserInterface(self.parser_version).parse_response(response)
            ParsedResponse.objects.create(
                response=response,
                parsed_response=parsed,
                coder_id=self.coder.id,
                parser=self.parser_version
            )
            return parsed
        except Exception as e:
            ParsedResponse.objects.create(
                response=response,
                parsed_response={},
                coder_id=self.coder.id,
                parser=self.parser_version,
                error={ "exception": str(type(e)), "message": e.args[0] }
            )
            print("*"*50)
            print("failed parse")
            print(str(type(e)))
            print(e.args[0])
            print("*"*50)
            raise e

    def __prompt_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, 'prompts', self.prompt_version)
