from .base import Base

class AskQuestion(Base):
    @classmethod
    def required_arguments(cls):
        return ["question"]
    
    def execute(self, question):
        return input(f"{question}").rstrip('\n')
    
    def convert_args_from_strings(self, arguments):
        return arguments