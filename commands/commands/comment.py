from .base import Base

class Comment(Base):
    def required_arguments(cls):
        return ["comment"]
    
    def convert_args_from_strings(self, arguments):
        return arguments
    
    def execute(self, comment):
        print(comment)