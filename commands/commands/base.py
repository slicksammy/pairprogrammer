from coder.exceptions import MissingArgumentsException

class Base:
    def __init__(self, arguments):
        self.arguments = arguments

    def required_arguments(cls):
        raise Exception("method not defined")
    
    def execute(self, **arguments):
        raise Exception("method not defined")

    def convert_args_from_strings(self, arguments):
        return arguments
     
    def custom_validations(self):
        return {}
    
    @classmethod
    def is_system(self):
        return False