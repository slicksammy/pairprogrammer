import os
from .parsers.interface import Interface as ParserInterface
from .tasks.interface import Interface as TaskInterface
from ..models import ParsedResponse
from json.decoder import JSONDecodeError
import textwrap

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
            return ParsedResponse.objects.create(
                response=response,
                parsed_response=parsed,
                coder_id=self.coder.id,
                parser=self.parser_version
            )
        except Exception as e:
            record = ParsedResponse.objects.create(
                response=response,
                parsed_response={},
                coder_id=self.coder.id,
                parser=self.parser_version,
                error={ "class": str(type(e)), "message": e.args[0] }
            )
            print("*"*50)
            print("failed parse")
            print(str(type(e)))
            print(e.args[0])
            print("*"*50)
            return record
        
    def client_exception(self, exception_class, exception_message):
        return exception_message
        
    def parse_recovery_message(self, parsed_object):
        error = parsed_object.error
        if error.get("class") == str(JSONDecodeError):
            return textwrap.dedent("""
            I was unable to parse your response and could not determine a command.
            For the next message only, repeat your previous message without a command.
            """).strip()
        else:
            return textwrap.dedent(f"""
            I was not able to parse your response.
            {error.get("message")[:50]}
            """).strip()

    def __prompt_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, 'prompts', self.prompt_version)
