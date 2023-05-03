# when a command is missing arguments
class MissingArgumentsException(Exception):
    pass

class InvalidArgumentsException(Exception):
    pass

class InvalidAssistantResponseException(Exception):
    pass

class NotEnoughTokensException(Exception):
    pass