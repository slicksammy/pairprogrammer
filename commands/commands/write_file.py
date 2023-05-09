from .base import Base
from django.conf import settings
import os
from commands.helpers import is_relative

class WriteFile(Base):
    def required_arguments(cls):
        return ["file_path", "content"]

    def convert_args_from_strings(self, arguments):
        return {
            "file_path": arguments["file_path"],
            "content": arguments["content"],
        }
    
    def custom_validations(self):
        if is_relative(self.arguments["file_path"]):
            return { "file_path": ["cannot be relative and may not start with .."] }
        else:
            return {}