from .base import Base
from django.conf import settings

class Python(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "python",
            "description": "run a python command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "will run python + command"
                    }
                },
                "required": ["command"],
            }
        }

    def required_arguments(cls):
        return ["command"]