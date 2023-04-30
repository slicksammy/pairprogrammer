from .base import Base
import os
from django.conf import settings

class CreateFile(Base):
    @classmethod
    def required_arguments(cls):
        return ["file_path"]
    
    def convert_args_from_strings(self, arguments):
        return arguments
    
    def execute(self, file_path):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        with open(absolute_path, 'w') as file:
            pass