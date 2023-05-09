from .base import Base
import os
from django.conf import settings
from commands.helpers import is_relative

class CreateDirectory(Base):
    def required_arguments(cls):
        return ["directory_path"]
    
    def execute(self, file_path):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        os.mkdirs(absolute_path)

    def custom_validations(self):
        if not is_relative(self.arguments["directory_path"]):
            return { "directory_path": ["must be relative and may not start with .."] }
        else:
            return {}