from .base import Base
from django.conf import settings
from commands.helpers import is_relative

class Mv(Base):
    def required_arguments(cls):
        return ["source", "destination"]
    
    def custom_validations(self):
        validations = {}
        if is_relative(self.arguments["source"]):
            validations["source"] = ["cannot be relative and may not start with .."]
        if is_relative(self.arguments["destination"]):
            validations["destination"] = ["cannot be relative and may not start with .."]
        
        return validations