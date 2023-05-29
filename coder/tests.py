from django.test import TestCase
from .interface import Interface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder
from unittest.mock import patch
from .response_parsers.gabe import Gabe
from .prompts.interface import Interface as PromptInterface

# Create your tests here.