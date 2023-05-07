from .base import Base
from django.conf import settings

class Rails(Base):
    def required_arguments(cls):
        return ["command"]