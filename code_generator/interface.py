import functools
from code_generator.response_parsers.xml import Xml
from code_generator.exceptions import MissingArgumentsException, CommandNotFoundException
from code_generator.commands import *


class Interface:
    def __init__(self):
        self.response_parser = "xml"
        self.successful_commands = []
        self.summaries = []
        self.created_files = set([])
        self.updated_files = set([])
        self.deleted_files = set([])
        self.current_task_index = 0

        self.messages = []
    
    @functools.cache
    def system_message(self):
        return { "role": "system", "content": self.build_prompt(), "error": False }
    
    def build_prompt(self):
        return self.base_prompt().replace("<<CONTEXT>>", self.context()).replace("<<REQUIREMENTS>>", self.requirements()).replace("<<RESPONSE_PROMPT", self.response_prompt()).replace("<<TASKS>>", "\n".join(self.tasks()))
    
    def context(self):
        return """
        Ruby on rails probject. Ruby 3.1.2p20 (2022-04-12 revision 4491bb740a) [arm64-darwin21].
        """

    def requirements(self):
        return """
        - Rewrite lib/agi_interface.rb in python
        """

    def response_prompt(self):
       return self.response_parser_class().response_prompt
    
    def tasks(self):
        return [
            "Write a function that takes a URL as input.",
            "Use Nokogiri to send an HTTP request and scrape the HTML document.",
            "Parse the HTML document to extract all text elements, including any text within child elements.",
            "Using regular expressions, count the number of times the word \"google\" appears in the scraped text.",
            "Find and visit all internal links on the page.",
            "Repeat steps 3-5 for each internal link in a recursive manner.",
            "Output the total count of the word \"google\" in the initial URL and all links.",
            "Test the function with sample input.",
            "Modify the function to take user input for the URL if desired.",
            "Write unit tests for the function to ensure it works correctly.",
        ]        
    
    def append_message(self, content, role="user", error=False, task=False):
        self.messages.append({ "role": role, "content": content, error: error, task: task})

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
        return Xml

    def exec_command(self, command, arguments):
        if command == "delete_file":
            klass, use_output, custom_output = [DeleteFile, False, "File deleted"]
        elif command == "view_changes":
            klass, use_output, custom_output = [ViewChanges, True, None]
        elif command == "delete_lines":
            klass, use_output, custom_output = [DeletLines, False, "Lines deleted"]
        elif command == "rspec":
            klass, use_output, custom_output = [Rspec, True, None]
        elif command == "ask_question":
            klass, use_output, custom_output = [AskQuestion, True, None]
        elif command == "read_file":
            klass, use_output, custom_output = [ReadFile, True, None]
        elif command == "update_file":
            klass, use_output, custom_output = [UpdateFile, False, "File updated"]
        elif command == "create_file":
            klass, use_output, custom_output = [CreateFile, False, "File created"]
        else:
            raise CommandNotFoundException(f"{command} not found")
            
        command_instance = klass()
        command_instance.validate_arguments(arguments)
        command_output = command_instance.execute(**arguments)
        if use_output:
            return command_output
        else:
            return custom_output


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
            - "undo"
                arguments: {}
                description: undo the last command
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
            - "task_completed"
                arguments:
                    "task": the task you just completed
                description: you are done with the current task and are ready to move on to the next one
            
            You may only use these commands.

        RESPONSE FORMAT:
            - You may only respond commands
            - You may only respond with one command at a time
            - You must include the arguments
            
            <<RESPONSE_PROMPT>>
        """
