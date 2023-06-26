from .base import Base
import os
from django.conf import settings
from commands.helpers import is_relative

class CreateDirectory(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "create_directory",
            "description": "create a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "The path to the directory to be created."
                    }
                },
                "required": ["directory_path"],
            }
        }

    def required_arguments(cls):
        return ["directory_path"]
    
    def execute(self, directory_path):
        absolute_path = os.path.join(settings.BASE_DIR, directory_path)
        os.makedirs(absolute_path)

    def custom_validations(self):
        if not is_relative(self.arguments["directory_path"]):
            return { "directory_path": ["must be relative and may not start with .."] }
        else:
            return {}
