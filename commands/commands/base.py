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
    
    @classmethod
    def parse_json(cls, initial_json, parse_to_json):
        parsed_json = {}
        
        for key, value in parse_to_json.items():
            if isinstance(value, dict):
                parsed_json[key] = cls.parse_json(initial_json.get(key, {}), value)
            else:
                parsed_json[key] = initial_json.get(key)
        
        return parsed_json