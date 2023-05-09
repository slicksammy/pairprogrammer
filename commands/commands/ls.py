from .base import Base
from django.conf import settings
from commands.helpers import is_relative

class Ls(Base):
    def required_arguments(cls):
        return []
    
    def custom_validations(self):
        if self.arguments.get("directory_path") and not is_relative(self.arguments["directory_path"]):
            return { "directory_path": ["must be relative and may not start with .."] }
        else:
            return {}