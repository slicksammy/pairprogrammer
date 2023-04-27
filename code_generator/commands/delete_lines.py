from commands import Base
from django.conf import settings
import os
from exceptions import InvalidArgumentException

class DeleteLines(Base):
    @classmethod
    def delete_lines(cls):
        return ["line_numbers"]
    
    def execute(self, file_path, line_numbers):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)

        with open(absolute_path, "r") as file:
            lines = file.readlines()

        lines = [line for index, line in enumerate(lines) if index not in line_numbers]

        with open(file_path, "w") as file:
            file.write("".join(lines))

    def __custom_validations(self, arguments):
        if len(arguments["line_numbers"]) < 1:
            raise InvalidArgumentException("line_numbers must include at least one line")