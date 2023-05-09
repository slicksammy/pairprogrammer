from .base import Base
import os
from django.conf import settings
from commands.helpers import is_relative

class DeleteFile(Base):
    def required_arguments(cls):
        return ["file_path"]
    
    def execute(self, file_path):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        os.remove(absolute_path)

    def custom_validations(self):
        if is_relative(self.arguments["file_path"]):
            return { "file_path": ["cannot be relative and may not start with .."] }
        else:
            return {}