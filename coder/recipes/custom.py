import json
from completions.interface import Interface as CompletionsInterface
from json.decoder import JSONDecodeError
from coder.models import CoderMessage
from commands.commands import Recall as RecallCommand
from commands.commands import Remember as RememberCommand
from commands.interface import Interface as CommandsInterface

class Custom:
    def __init__(self, coder, config):
        self.coder = coder
        self.prompt = config["prompt"]
        self.functions = config["functions"]
        self.model = config["model"]

    def after_create(self):
        content =  self.prompt.replace("<<REQUIREMENTS>>", self.coder.requirements)

        CoderMessage.objects.create(
            coder = self.coder,
            role = "user",
            function_name = None,
            content = content,
            function_call = None
        )

    def before_run(self, message):
        if message.command_error is not None:
            if message.command_error.get("code") == "missing_command":
                CoderMessage.objects.create(
                    coder = self.coder,
                    role = "user",
                    function_name = None,
                    content = "I was not able to parse the json. Please repeat useing the \"comment\" command",
                    function_call = None
                )
            elif message.command_error.get("code") == "invalid_command":
                CoderMessage.objects.create(
                    coder = self.coder,
                    role = "user",
                    function_name = None,
                    content = "The command you provided is invalid",
                    function_call = None
                )
            elif message.command_error.get("code") == "invalid_arguments":
                CoderMessage.objects.create(
                    coder = self.coder,
                    role = "user",
                    function_name = None,
                    content = f'There was an error with your arguments: {message.command_error.get("validation_errors")}',
                    function_call = None
                )

    def on_function_call(self, output, command_name):
        CoderMessage.objects.create(
            coder=self.coder,
            role="function",
            function_name=command_name,
            content=output,
            function_call=None
        )

        # if last_message.command and last_message.command.get("complete"):
        #     next_task = coder.current_task_index + 1

    def on_run(self, user):
        messages = []
        for message in CoderMessage.objects.filter(coder=self.coder).order_by("created_at"):
            if message.role == "user":
                messages.append(
                    {
                        "role": "user",
                        "content": message.content
                    }
                )
            elif message.role == "assistant":
                if message.function_call is not None:
                    messages.append(
                        {
                            "role": "assistant",
                            "content": message.content,
                            "function_call": json.loads(message.function_call)
                        }
                    )
                else:
                    messages.append(
                         {
                            "role": "assistant",
                            "content": message.content,
                         }
                    )
            elif message.role == "function":
                messages.append(
                    {
                        "role": "function",
                        "name": message.function_name,
                        "content": message.content
                    }
                )

        # TODO get functions
        functions = [CommandsInterface.get_command(function) for function in self.functions]
        functions = [function.schema() for function in functions]
        return CompletionsInterface.create_completion(user=user, use_case="coder_completion", messages=messages, model=self.model, functions=functions, function_call="auto")

    def get_completion_message(self, completion):
        return completion.message

    def parse_command_from_message(self, message):
        if message.get("function_call"):
            try:
                return {
                    "command": message["function_call"]["name"],
                    "arguments": json.loads(message["function_call"]["arguments"])
                }
            except JSONDecodeError:
                return None
        else:
            return {
                "command": "comment",
                "arguments": {
                    "comment": message["content"]
                }
            }

    