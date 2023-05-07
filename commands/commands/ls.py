from .base import Base
from django.conf import settings

class Ls(Base):
    def required_arguments(cls):
        return []