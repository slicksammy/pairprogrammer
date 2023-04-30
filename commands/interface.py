from .exceptions import CommandNotFoundException
from commands.commands import *

class Interface:
    def exec_command(self, command, arguments):
        if command == "delete_file":
            klass, use_output, custom_output = [DeleteFile, False, "File deleted"]
        elif command == "view_changes":
            klass, use_output, custom_output = [ViewChanges, True, None]
        elif command == "delete_lines":
            klass, use_output, custom_output = [DeleteLines, False, "Lines deleted"]
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
        elif command == "create_directory":
            klass, use_output, custom_output = [CreateDirectory, False, "Directory created"]
        else:
            raise CommandNotFoundException(f"{command} not found")
        
        try:
            command_instance = klass()
            command_instance.validate_arguments(arguments)
            arguments = command_instance.convert_args_from_strings(arguments)
            command_output = command_instance.execute(**arguments)
            if use_output:
                output = command_output
            else:
                output = custom_output
            return { "output": output, "exception": False }
        except Exception as e:
            return { "type": str(type(e)), "message": e.args[0], "exception": True }

