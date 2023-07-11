from .base import Base
import requests
from django.conf import settings
from commands.helpers import is_relative
from integrations.interface import Interface as IntegrationsInterface


class RailwayGetInformation(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "railway_get_information",
            "description": "get information about a Railway project via the Railway API",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "The ID of the Railway project"
                    }
                },
                "required": ["project_id"],
            }
        }

    def required_arguments(cls):
        return ["project_id"]
    
    @classmethod
    def is_system(cls):
        return True

    @classmethod
    def run(cls, arguments, user):
        config = IntegrationsInterface.get_config(user=user, integration_identifier='railway')
        if config is None:
            raise Exception("You need to configure the railway integration first")
        
        access_token = config['api_key']

        project_id = config['project_id']

        url = f"https://backboard.railway.app/graphql/v2"

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

        data = {'query':"query project {\n  project(id: \"" + project_id + "\") {\n    id\n    name\n    plugins {\n      edges {\n        node {\n          id\n          name\n        }\n      }\n    }\n    environments {\n      edges {\n        node {\n          id\n          name\n        }\n      }\n    }\n    services {\n      edges {\n        node {\n          id\n          name\n          deployments {\n            edges {\n              node {\n                id\n                status\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}"}

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        # json = response.json()
        # if response.status_code == 200:
        #     json = [cls.parse_json(comment, cls.parse_fields()) for comment in json]

        print('*'*50)
        print('Railway response')
        print(response.json())
        print('Parsed response')
        # print(json)

        return response.json()
