from .base import Base
from django.conf import settings

class Bundle(Base):
    def required_arguments(cls):
        return ["command"]