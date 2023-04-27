from exceptions import MissingArgumentsException

class Base:
    @classmethod
    def required_arguments(cls):
        raise Exception("method not defined")
    
    def validate_arguments(self, arguments):
        self.__validate_required_arguments(arguments)
        self.__custom_validations(arguments)
    
    def execute(self, **arguments):
        raise Exception("method not defined")
     
    def __custom_validations(self, arguments):
        pass
    
    def __validate_required_arguments(self, arguments):
        required_arguments = type(self).required_arguments()
        missing_arguments = []

        for argument in required_arguments:
            if arguments[argument] is None:
                missing_arguments << argument

        if len(missing_arguments) > 0:
            raise MissingArgumentsException(f'Missing arguments: {(", ").join(missing_arguments)}')