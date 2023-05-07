from .base import Base
from django.conf import settings

class Python(Base):
    def required_arguments(cls):
        return ["command"]