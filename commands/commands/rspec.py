from .base import Base
import subprocess
from django.conf import settings
import os

class Rspec(Base):
    def required_arguments(cls):
        return ["file_path"]
    
    def execute(self, file_path):
        absolute_path = os.path.join(settings.BASE_DIR, file_path)
        subprocess.check_output(["rspec", absolute_path], universal_newlines=True)