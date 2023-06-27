from .base import Base
from django.conf import settings
from vectordb.interface import Interface as VectorInterface

class Remember(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "remember",
            "description": "will save a thought to your memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "thought": {
                        "type": "string",
                        "description": "the thought to be saved"
                    }
                },
                "required": ["thought"],
            }
        }

    def required_arguments(cls):
        return ["thought"]
    
    @classmethod
    def is_system(self):
        return True

    @classmethod
    def run(self, arguments, user):
        thought = arguments["thought"]

        vector = VectorInterface.embed(thought, user)
        
        interface = VectorInterface(user)
        interface.add_point(vector, { "content": thought })
        return "Memory Saved"