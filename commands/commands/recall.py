from .base import Base
from django.conf import settings
from vectordb.interface import Interface as VectorInterface

class Recall(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "recall",
            "description": "will search through your memory and return relevant information",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "will search through your memory on a given topic and return relevant memories"
                    }
                },
                "required": ["topic"],
            }
        }

    def required_arguments(cls):
        return ["topic"]
    
    @classmethod
    def is_system(self):
        return True

    @classmethod
    def run(self, arguments, user):
        topic = arguments["topic"]

        vector = VectorInterface.embed(topic, user)

        interface = VectorInterface(user)
        matches = interface.search(vector)["matches"]
        return {
            "matches": matches
        }