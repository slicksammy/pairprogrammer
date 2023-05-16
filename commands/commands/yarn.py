from .base import Base
from django.conf import settings

class Yarn(Base):
    def required_arguments(cls):
        return ["command"]