# when a command is missing arguments
class MissingArgumentsException(Exception):
    pass

class InvalidArgumentException(Exception):
    pass

class CommandNotFoundException(Exception):
    pass