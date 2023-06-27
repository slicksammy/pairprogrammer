import json
from ..models import Coder
from completions.interface import Interface as CompletionsInterface
from app_messages.interface import Interface as MessagesInterface
from json.decoder import JSONDecodeError
from coder.models import CoderMessage
import textwrap
from commands.commands import ReadFile, WriteFile, Rails, CreateFile, CreateDirectory

class FunctionCall:
    def __init__(self, coder, config):
        self.coder = coder
        self.model = config["model"]

    def after_create(self):
        content =  """
        You are an AI assistant that follows instructions extremely well. Help as much as you can.

        The user is building a feature:

        REQUIREMENTS:
        <<REQUIREMENTS>>

        TASKS:
        <<TASKS>>

        Information about the application:
        <<CONTEXT>>
        
        """.replace("<<CONTEXT>>", self.coder.context).replace("<<REQUIREMENTS>>", self.coder.requirements).replace("<<TASKS>>", "\n".join(self.coder.tasks))

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

    def on_function_call(self, output, command, last_message):
        CoderMessage.objects.create(
            coder=self.coder,
            role="function",
            function_name=command,
            content=output,
            function_call=None
        )

        # if last_message.command and last_message.command.get("complete"):
        #     next_task = coder.current_task_index + 1

    def on_run(self):
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
        functions = [ReadFile.schema(), WriteFile.schema(), Rails.schema(), CreateFile.schema(), CreateDirectory.schema()]
        return CompletionsInterface.create_completion(self.coder.id, messages, self.model, functions, function_call="auto") #gpt-3.5-turbo-16k-0613

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

    