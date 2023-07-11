from .base import Base
import requests
from django.conf import settings
from commands.helpers import is_relative
from integrations.interface import Interface as IntegrationsInterface

class ListGitHubPullRequest(Base):
    @classmethod
    def schema(cls):
        return {
            'name': 'list_github_pull_request',
            'description': 'Get a list of pull requests from the GitHub API',
            'parameters': {
                'type': 'object',
                'properties': {
                    'owner': {
                        'type': 'string',
                        'description': 'Owner of the repository - only use if user has specified an owner otherwise leave blank'
                    },
                    'repo': {
                        'type': 'string',
                        'description': 'Repository name - only use if user has specified an owner otherwise leave blank'
                    }
                },
                'required': [],
            }
        }

    def required_arguments(cls):
        return []
    
    @classmethod
    def is_system(self):
        return True
    

    @classmethod
    def parse_fields(self):
        return {
            "id": None,
            "url": None,
            "state": None,
            "body": None,
            "created_at": None,
            "closed_at": None,
            "merged_at": None,
            "title": None,
            "repo": {
                "owner": None,
                "repo": None
            },
            "head": {
                "ref": None,
            }
        }

    @classmethod
    def run(cls, arguments, user):
        config = IntegrationsInterface.get_config(user=user, integration_identifier='github')
        if config is None:
            raise Exception('You need to configure the GitHub integration first')
        
        api_token = config['api_key']

        # Replace with your repository owner and name
        owner = arguments.get('owner') or config.get('owner')
        if owner is None:
            raise Exception('You need to specify an owner')

        repo = arguments.get('repo') or config.get('repo')
        if repo is None:
            raise Exception('You need to specify a repo')

        url = f'https://api.github.com/repos/{owner}/{repo}/pulls'

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {api_token}',
            'X-Github-Api-Version': '2022-11-28'
        }

        response = requests.get(
            url,
            headers=headers
        )
        
        json = response.json()
        if response.status_code == 200:
            json = [cls.parse_json(pull, cls.parse_fields()) for pull in json]

        print('*'*50)
        print('GitHub response')
        print(response.json())
        print('Parsed response')
        print(json)

        return json