from .exceptions import CommandNotFoundException
from commands.commands import *

class Interface:
    COMMANDS = {
        "delete_file": DeleteFile,
        "view_changes": ViewChanges,
        "delete_lines": DeleteLines,
        "rspec": Rspec,
        "ask_question": AskQuestion,
        "read_file": ReadFile,
        "update_file": UpdateFile,
        "create_file": CreateFile,
        "create_directory": CreateDirectory,
        "comment": Comment,
        "write_file": WriteFile,
        "rails": Rails,
        "bundle": Bundle,
        "ls": Ls,
    }

    @classmethod
    def validate_arguments(cls, command, arguments):
        command_instance = cls.COMMANDS[command](arguments)
        validations = {}
        # get the required arguments
        for argument in command_instance.required_arguments():
            if arguments.get(argument) is None:
                validations[argument] = ["missing"]
        
        for argument, errors in command_instance.custom_validations().items():
            if validations.get(argument):
                validations[argument] += errors
            else:
                validations[argument] = errors
            
        return validations
    

    # def exec_command(self, command, arguments):
    #     if command == "delete_file":
    #         klass, use_output, custom_output = [DeleteFile, False, "File deleted"]
    #     elif command == "view_changes":
    #         klass, use_output, custom_output = [ViewChanges, True, None]
    #     elif command == "delete_lines":
    #         klass, use_output, custom_output = [DeleteLines, False, "Lines deleted"]
    #     elif command == "rspec":
    #         klass, use_output, custom_output = [Rspec, True, None]
    #     elif command == "ask_question":
    #         klass, use_output, custom_output = [AskQuestion, True, None]
    #     elif command == "read_file":
    #         klass, use_output, custom_output = [ReadFile, True, None]
    #     elif command == "update_file":
    #         klass, use_output, custom_output = [UpdateFile, False, "File updated"]
    #     elif command == "create_file":
    #         klass, use_output, custom_output = [CreateFile, False, "File created"]
    #     elif command == "create_directory":
    #         klass, use_output, custom_output = [CreateDirectory, False, "Directory created"]
    #     elif command == "comment":
    #         klass, use_output, custom_output = [Comment, False, "Comment displayed"]
    #     else:
    #         raise CommandNotFoundException(f"{command} not found")
        
    #     try:
    #         command_instance = klass()
    #         command_instance.validate_arguments(arguments)
    #         # arguments = command_instance.convert_args_from_strings(arguments)
    #         command_output = command_instance.execute(**arguments)
    #         if use_output:
    #             output = command_output
    #         else:
    #             output = custom_output
    #         return { "output": output, "exception": False }
    #     except Exception as e:
    #         return { "type": str(type(e)), "message": e.args[0], "exception": True }

