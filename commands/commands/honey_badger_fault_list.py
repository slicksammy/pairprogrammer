from .base import Base
import requests
from django.conf import settings
from commands.helpers import is_relative
from integrations.interface import Interface as IntegrationsInterface

class HoneyBadgerFaultList(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "honey_badger_fault_list",
            "description": "get a list of faults from the honey badger api",
            "parameters": {
                "type": "object",
                "properties": {
                    "recent": {
                        "type": "boolean",
                        "description": "List the errors that have most recently occurred first"
                    },
                    "frequent": {
                        "type": "boolean",
                        "description": "List the errors that have occurred most frequently first"
                    }
                },
                "required": ["recent", "frequent"],
            }
        }

    def required_arguments(cls):
        return ["recent", "frequent"]
    
    @classmethod
    def is_system(self):
        return True

    @classmethod
    def run(self, arguments, user):
        config = IntegrationsInterface.get_config(user=user, integration_identifier='honeybadger')
        if config is None:
            raise Exception("You need to configure the honeybadger integration first")
        
        api_key = config['api_key']

        # Replace with your project ID
        project_id = config['project_id']

        url = f"https://app.honeybadger.io/v2/projects/{project_id}/faults"

        params = {
            'recent': arguments['recent'],
            'frequent': arguments['frequent']
        }

        response = requests.get(
            url,
            params=params,
            auth=(api_key, ''),
        )

        print("*"*50)
        print("Honeybader response")
        print(response.json())
        
        return response.json()