import functools
from code_generator.response_parsers.xml import Xml
from code_generator.response_parsers.line import Line
from code_generator.exceptions import InvalidAssistantResponseException
from commands.interface import Interface as CommandInterface
from completions.interface import Interface as CompletionsInterface
import pdb
# TODO: move to environment variable - this is my personal key

class Interface:
    def __init__(self):
        self.response_parser = "line"
        self.successful_commands = []
        self.summaries = []
        self.created_files = set([])
        self.updated_files = set([])
        self.deleted_files = set([])
        self.current_task_index = 0

        self.messages = [self.system_message()]
        self.append_task_message()

    def run_command(self):
        last_message = self.messages[-1]
        if last_message["role"] == "assistant":
            content = last_message["content"]
            try:
                parsed_response = self.__parse_response(content)

                command = parsed_response["command"]
                arguments = parsed_response["arguments"]
                summary = parsed_response["summary"]
                explanation = parsed_response["explanation"]
                task = parsed_response["task"]
                complete = parsed_response["complete"]

                print("*"*50)
                print(f"command: {command}")
                print(f"arguments: {arguments}")
                print(f"summary: {summary}")
                print(f"explanation: {explanation}")
                print(f"task: {task}")
                print(f"task: {complete}")
                print("*"*50)

                response = CommandInterface().exec_command(command, arguments)
                if response["exception"]:
                    self.__mark_previous_message_as_error()
                    e_type = response["type"]
                    e_message = response["message"]
                    self.__append_exception(e_type, e_message)
                    print("*"*50)
                    print("command failed")
                    print(e_type)
                    print(e_message)
                    print("*"*50)
                    self.summaries.append(summary)
                    self.successful_commands.append({ "command": command, "arguments": arguments })
                else:
                    output = response["output"]
                    self.__append_output(output)
                    print("*"*50)
                    print("command succeeded")
                    print(output)
                    print("*"*50)

            except Exception as e:
                print("*"*50)
                print("exception")
                print(e.args[0])
                print("*"*50)
                self.__mark_previous_message_as_error()
                self.__append_exception(type(e), e.args[0])
        
        if complete:
            self.next_task()

    def run(self):
        self.run_completion()
        self.run_command()

    def skip_task(self):
        self.next_task()

    def cleanup_file(self, file_path, model="gpt-4"):
        file_contents = CommandInterface().exec_command("read_file", { "file_path": file_path })["output"]
        content = "\n".join([f"This is file {file_path} and here are the contents", file_contents, "Cleanup any syntax errors and return just the updated file contents, no additional characters"])
        completions_interface = CompletionsInterface()
        new_file_contents = completions_interface.run_completion([{ "role": "user", "content": content }], model)
        lines = new_file_contents.split("\n")
        if lines[0].startswith("```"):
            lines.pop(0)
        if lines[-1].startswith("```"):
            lines.pop
        new_file_contents = "\n".join(lines)
        CommandInterface().exec_command("create_file", { "file_path": file_path })
        CommandInterface().exec_command("update_file", { "file_path": file_path, "content": new_file_contents, "line_number": 0 })
            
    def __append_output(self, output):
        content = f"""
        Your previous command executed successfully.
        COMMAND OUTPUT: {output}
        Continue
        """

        self.append_message(content)

    def __append_exception(self, e_type, e_message):
        content = f"{e_type} {e_message[:100]}"
        self.append_message(content, role="user", error=True)

    def __mark_previous_message_as_error(self):
        self.messages[-1]["error"] = True

    def run_completion(self, model="gpt-4"):
        formatted_messages = [{"content": message["content"], "role": message["role"]} for message in self.messages]
        completions_interface = CompletionsInterface()
        if completions_interface.available_completion_tokens(formatted_messages, model) > 200:
            content = CompletionsInterface().run_completion(formatted_messages, model)
            self.append_message(content, role="assistant")
            return content
        else:
            pdb.set_trace()
        
    
    @functools.cache
    def system_message(self):
        return { "role": "system", "content": self.build_prompt(), "error": False, "task": False }
    
    def build_prompt(self):
        return self.base_prompt().replace("<<CONTEXT>>", self.context()).replace("<<REQUIREMENTS>>", self.requirements()).replace("<<RESPONSE_PROMPT", self.response_prompt()).replace("<<TASKS>>", "\n".join(self.tasks()))
    
    def context(self):
        return """
        Ruby on rails probject. Ruby 3.1.2p20 (2022-04-12 revision 4491bb740a) [arm64-darwin21].
        """

    def requirements(self):
        return """
        - I need to build a ruby cli
        """

    def response_prompt(self):
       return self.response_parser_class().response_prompt()
    
    def tasks(self):
        return ['Create a new Ruby file called `pairprogrammer.rb`',
                'Define a new class called `Planner` within the `pairprogrammer.rb` file',
                'Within the `Planner` class, define a new method called `respond(message)`, which will use the `Net::HTTP` library to send an HTTP POST request to the pre-configured URL with the `message` as the request body',
                'Implement command-line argument parsing in the `pairprogrammer.rb` file',
                'In the `pairprogrammer.rb` file, define logic for parsing the command `planner respond MESSAGE` and calling the appropriate method from the `Planner` class',
                'Create a `README.md` file with documentation and installation instructions',
                'Add a `--help` option to the command-line arguments in order to display a help message when it is used',
                'Test the CLI thoroughly to ensure it meets all requirements']       
    
    def append_message(self, content, role="user", error=False, task=False):
        self.messages.append({ "role": role, "content": content, "error": error, "task": task })

    def give_feedback(self, content):
        content = f"""
        I have some feedback regarding the current task:
        {content}

        Please continue responding with commands to address my feedback
        """

        self.append_message(content)

    def append_task_message(self):
        task = self.tasks()[self.current_task_index]
        content = f"""
        TASK: {task}
        """
        
        self.append_message(content, role="user", error=False, task=True)

    def next_task(self):
        if self.current_task_index == len(self.tasks()) - 1:
            return False
        else:
            self.current_task_index += 1
            self.append_task_message()
            return True
    
    def response_parser_class(self):
        return Line
        
    def __parse_response(self, content):
        object = self.response_parser_class().parse_response_object(content)
        
        if object is None:
            raise InvalidAssistantResponseException("Your response is invalid. Please follow the detailed response format")

        parsed = self.response_parser_class().parse_object_to_dict(object)

        if parsed["command"] is None:
            raise InvalidAssistantResponseException("Could not find the command")

        if parsed["arguments"] is None:
            raise InvalidAssistantResponseException("Could not find the arguments")

        if parsed["summary"] is None:
            raise InvalidAssistantResponseException("Could not find the summary")
        
        if parsed["complete"] is None:
            raise InvalidAssistantResponseException("Could not find the complete")

        return parsed


    def base_prompt(self):
        return """
        You are given a set of requirements and will be asked to perform a series of tasks to complete the requirements. You can see the tasks below but I will present them to you one at a time to complete.
        You can only respond with the commands listed below. If you need clarification, use the "ask_question" commmand. Once a task is completed, use the "task_completed" command to move on to the next task.

        REQUIREMENTS:
        <<REQUIREMENTS>>

        CONTEXT:
        <<CONTEXT>>

        TASKS:
        <<TASKS>>

        BEST PRACTICES:
            - Ask the user before adding any dependencies
            - requires should be at the top of the file
            - Do not update README.md
            - Tests go in spec/
            - When creating new files, always confirm the file path with the user

        RULES:
            - Respond with ONLY 1 command at a time
            - You must complete the tasks in order

        COMMANDS:
            - "create_directory"
                arguments:
                    "directory_path": the relative path to the directory
                description: creates a directory
            - "view_changes"
                arguments: {}
                description: shows the changes you've made so far
            - "delete_lines"
                arguments:
                    "file_path": the relative path to the file
                    "line_numbers": a list of line numbers to delete (0-indexed)
                        examples:
                            - [4,6,9,17] will delete lines 4,6,9,17
                            - [4] will delete line 4
                description: will delete lines from a file
            - "read_file"
                arguments: 
                    "file_path": the relative path to the file
                description: you can read any file from this project to get information
            - "update_file"
                arguments:
                    "file_path": the relative path to the file
                    "content": the content to write to the file
                    "line_number": which line in the file to insert the content
                description: will insert content into an existing file starting at the given line number. It will not overrite any existing content. To remove content use the delete_lines command.
            - "create_file"
                arguments:
                    "file_path": the relative path to the file
                description: creates a new file
            - "delete_file"
                arguments:
                    "file_path": the relative path to the file
            - "ask_question"
                arguments:
                    "question": the question to ask the user
                description: If you need clarification from the user you can use this command to ask a question. You can also ask for examples.
            - "rspec"
                arguments:
                    "file_path": the relative path to the file
                description: runs a single rspec test file
            
            You may only use these commands.

        RESPONSE FORMAT:
            - You may only respond commands
            - You may only respond with one command at a time
            - You must include the arguments
            
            <<RESPONSE_PROMPT>>
        """
