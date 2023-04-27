from commands import Base
import os
from django.conf import settings

class ReadFile(Base):
    @classmethod
    def required_arguments(cls):
        return ["file_path"]
    
    def execute(self, file_path):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        with open(absolute_path, "r") as file:
            return file.read()