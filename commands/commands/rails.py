from .base import Base
from django.conf import settings

class Rails(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "rails",
            "description": "run a rails command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "will run rails + command"
                    }
                },
                "required": ["command"],
            }
        }

    def required_arguments(cls):
        return ["command"]