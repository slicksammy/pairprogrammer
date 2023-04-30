from .base import Base
from django.conf import settings
import os

class UpdateFile(Base):
    @classmethod
    def required_arguments(cls):
        return ["file_path", "content", "line_number"]

    def convert_args_from_strings(self, arguments):
        return {
            "file_path": arguments["file_path"],
            "content": arguments["content"],
            "line_number": int(arguments["line_number"])
        }
    
    def execute(self, file_path, content, line_number):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        # TODO return which lines were inserted
        if line_number == -1:
            with open(absolute_path, "a") as file:
                file.write(content)
                file.write("\n")
        else:
            with open(absolute_path, "r") as file:
                lines = file.readlines()
            lines.insert(line_number, content)
            
            with open(absolute_path, "w") as file:
                for line in lines:
                    file.write(line)