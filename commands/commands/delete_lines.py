from .base import Base
from django.conf import settings
import os
from commands.exceptions import InvalidArgumentException
import json
from commands.helpers import is_relative

class DeleteLines(Base):
    def required_arguments(cls):
        return ["line_numbers", "file_path"]
    
    def convert_args_from_strings(self, arguments):
        return {
            "file_path": arguments["file_path"],
            "line_numbers": json.loads(arguments["line_numbers"])
        }
    
    def execute(self, file_path, line_numbers):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)

        with open(absolute_path, "r") as file:
            lines = file.readlines()

        lines = [line for index, line in enumerate(lines) if index not in line_numbers]

        with open(file_path, "w") as file:
            file.write("".join(lines))

    def custom_validations(self):
        validations = {}
        if len(self.arguments.get("line_numbers", 0)) < 1:
            validations["line_numbers"] = ["must include at least one line number"]

        if not is_relative(self.arguments["file_path"]):
            validations["file_path"] = ["must be relative and may not start with .."]
        
        return validations