from .base import Base
import os
from django.conf import settings
from commands.helpers import is_relative

class ReadFile(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "read_file",
            "description": "read a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to be read."
                    }
                },
                "required": ["file_path"],
            }
        }

    def required_arguments(cls):
        return ["file_path"]
    
    def convert_args_from_strings(self, arguments):
        return arguments
    
    def custom_validations(self):
        if not is_relative(self.arguments["file_path"]):
            return { "file_path": ["must be relative and may not start with .."] }
        else:
            return {}