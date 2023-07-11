from .base import Base
import requests
from django.conf import settings
from commands.helpers import is_relative
from integrations.interface import Interface as IntegrationsInterface

class HoneyBadgerFaultID(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "honey_badger_fault_id",
            "description": "get fault details by id from the honey badger api",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Fault ID"
                    }
                },
                "required": ["id"],
            }
        }

    def required_arguments(cls):
        return ["id"]

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

        fault_id = arguments['id']

        url = f"https://app.honeybadger.io/v2/projects/{project_id}/faults/{fault_id}/notices"

        response = requests.get(
            url,
            auth=(api_key, ''),
        )

        print("*"*50)
        print("Honeybader response")
        print(response.json())

        return response.json()
