from .base import Base
import os
from django.conf import settings
from commands.helpers import is_relative

class ReadFile(Base):
    def required_arguments(cls):
        return ["file_path"]
    
    def convert_args_from_strings(self, arguments):
        return arguments
    
    def custom_validations(self):
        if is_relative(self.arguments["file_path"]):
            return { "file_path": ["cannot be relative and may not start with .."] }
        else:
            return {}