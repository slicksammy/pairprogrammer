from .base import Base
import os
from django.conf import settings

class CreateDirectory(Base):
    def required_arguments(cls):
        return ["directory_path"]
    
    def execute(self, file_path):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        os.mkdirs(absolute_path)