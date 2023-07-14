from .exceptions import CommandNotFoundException
from commands.commands import *
from .config import Config

class Interface:
    @classmethod
    def choosable_commands(cls):
        ignore_these = []
        ignore_these.append('comment') # this command is allowed by default
        ignore_these.append('github_pull_comment_replies') # this command is only used for beta integration

        output = {}
        for command, configuration in Config.COMMANDS.items():
            if command not in ignore_these:
                output[command] = {
                    "display": configuration['display'],
                    "description": configuration['description'],
                    "group": configuration['group']
                }

        return output

    @classmethod
    def get_command(cls, command):
        return Config.get_command(command)['command_class']

    @classmethod
    def command_exists(cls, command):
        return Config.command_exists(command)

    @classmethod
    def validate_arguments(cls, command, arguments):
        command_instance = Config.get_command(command)['command_class'](arguments)
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
    
    @classmethod
    def is_system_command(cls, command):
        command_class = Config.get_command(command)['command_class']
        return command_class.is_system()

    @classmethod
    def run_system_command(cls, command, arguments, user):
        command_class = Config.get_command(command)['command_class']
        if not command_class.is_system():
            raise Exception("Not a system command")
        
        return command_class.run(arguments, user)
