import json
from ..models import Coder
from completions.interface import Interface as CompletionsInterface
from app_messages.interface import Interface as MessagesInterface
from json.decoder import JSONDecodeError
from coder.models import CoderMessage
import textwrap

class Original:
    def __init__(self, coder):
        self.coder = coder

    def after_create(self):
        content =  """
        Help me build my feature.

        REQUIREMENTS:
        <<REQUIREMENTS>>

        CONTEXT:
        <<CONTEXT>>

        TASKS:
        <<TASKS>>

        RULES:
            - Respond with ONLY 1 command at a time
            - You must complete the tasks in order

        COMMANDS:
            - "yarn"
                arguments:
                    "command":
                        description: the command to run after yarn
                        required: true
                description: will run yarn + command
            - "python"
                arguments:
                    "command":
                        description: the python command to run after python manage.py
                        required: true
                description: will run python manage.py + command in a django app
            - "ls"
                arguments:
                    "directory_path":
                        description: the relative path to the directory // if no directory is provided, it will list the current directory
                        required: true
                description: will list the contents of a directory
            - "bundle"
                arguments:
                    "command": 
                        description: the bundler command to run // everything after "bundle"
                        required: true
                description: will run bundle + command
            - "rails"
                arguments:
                    "command":
                        description: the rails command to run // everything after "rails"
                        required: true
                description: will run rails + command
            - "create_directory"
                arguments:
                    "directory_path":
                        description: the relative path to the directory
                        required: true
                description: creates a directory
            - "delete_lines"
                arguments:
                    "file_path":
                        description: the relative path to the file
                        required: true
                    "line_numbers":
                        description: a list of line numbers to delete (0-indexed)
                        required: true
                        examples:
                            - [4,6,9,17] will delete lines 4,6,9,17
                            - [4] will delete line 4
                description: will delete lines from a file
            - "read_file"
                arguments: 
                    "file_path":
                        description: the relative path to the file
                        required: true
                description: you can read any file from this project to get information
            - "write_file"
                arguments:
                    "file_path":
                        description: the relative path to the file
                        required: true
                    "content":
                        description: the content to write to the file
                        required: true
                description: will replace existing file content with "content". Make sure to first read the file and ammend it with the new content.
            - "create_file"
                arguments:
                    "file_path":
                        description: the relative path to the file
                        required: true
                description: creates a new file
            - "delete_file"
                arguments:
                    "file_path":
                        description: the relative path to the file
                        required: true
            - "ask_question"
                arguments:
                    "question":
                        description: the question to ask the user
                        required: true
                description: If you need clarification from the user you can use this command to ask a question. You can also ask for examples.
            - "comment"
                arguments:
                    "comment":
                        description: a comment that the user will see
                        required: true
                description: if you want to make a comment to the user, that does not perform any actions, use this command
            - "rspec"
                arguments:
                    "file_path":
                        description: the relative path to the file
                        required: true
                description: runs a single rspec test file
            
            You may only use these commands.

        RESPONSE FORMAT:
            - You may only respond with commands
            - You may only respond with one command at a time
            - You must include the arguments

            Respond with a ONLY a PYTHON JSON object with the following fields:
                
                "command": create_file (string)
                "arguments": {"file_path": "some/file_path.rb"} (json) // If there are no arguments, use an empty JSON object: {}
                "explanation": I need to create a new file (string)
                "summary": creating a file (string)
                "task": the task you are working on (string)
                "complete": if the current task has been completed (boolean)

                Example:
                {
                    "command": "create_file",
                    "arguments": {
                        "file_path": "some/file_path.rb"
                    },
                    "explanation": "I need to create a new file",
                    "summary": "creating a file",
                    "task": "the task you are working on",
                    "complete": false
                }
        """.replace("<<CONTEXT>>", self.coder.context).replace("<<REQUIREMENTS>>", self.coder.requirements).replace("<<TASKS>>", "\n".join(self.coder.tasks))

        breakpoint()

        CoderMessage.objects.create(
            coder = self.coder,
            role = "user",
            function_name = None,
            content = content,
            function_call = None
        )

        CoderMessage.objects.create(
            coder = self.coder,
            role = "user",
            function_name = None,
            content = f"TASK: {self.coder.tasks[0]}",
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
            role="user",
            function_name=None,
            content=f'Output: {output}',
            function_call=None
        )

        # if last_message.command and last_message.command.get("complete"):
        #     next_task = coder.current_task_index + 1

    def on_run(self):
        messages = CoderMessage.objects.filter(coder=self.coder).order_by("created_at")
        messages = [{ "role": message.role, "content": message.content } for message in messages]
        
        return CompletionsInterface.create_completion(self.coder.id, messages, "gpt-4")

    def get_completion_message(self, completion):
        return completion.message

    def parse_command_from_message(self, message):
        content = message["content"]
        command = None
        try:
            # these 3 check if it is a command
            content.index("command")
            content.index("arguments")
            content.index("explanation")

            start_index = content.index("{")  # find the first occurrence of the opening brace
            end_index = content.rindex("}")  # find the last occurrence of the closing brace
            json_string = content[start_index:end_index+1]
            command = json.loads(json_string)
        except JSONDecodeError:
            pass
        except ValueError:
            # content.index will throw a ValueError exception so we will just return the entire content as explanation
            command = {
                "command": "comment",
                "arguments": {
                    "comment": content
                } 
            }
        
        return command
    