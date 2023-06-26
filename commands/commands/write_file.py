from .base import Base
from django.conf import settings
import os
from commands.helpers import is_relative

class WriteFile(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "write_file",
            "description": "writes content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to be read."
                    },
                    "content": {
                        "type": "string",
                        "description": "the contents of the file"
                    }
                },
                "required": ["file_path", "content"],
            }
        }
    
    def required_arguments(cls):
        return ["file_path", "content"]

    def convert_args_from_strings(self, arguments):
        return {
            "file_path": arguments["file_path"],
            "content": arguments["content"],
        }
    
    def custom_validations(self):
        if not is_relative(self.arguments["file_path"]):
            return { "file_path": ["must be relative and may not start with .."] }
        else:
            return {}