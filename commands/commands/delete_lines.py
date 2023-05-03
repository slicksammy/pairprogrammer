from .base import Base
from django.conf import settings
import os
from commands.exceptions import InvalidArgumentException
import json

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
        # missing validation will catch this
        if len(self.arguments.get("line_numbers", 0)) < 1:
            return { "line_numbers": ["must include at least one line number"] }
        else:
            return {}