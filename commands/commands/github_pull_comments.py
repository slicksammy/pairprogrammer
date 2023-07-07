from .base import Base
import requests
from django.conf import settings
from commands.helpers import is_relative
from integrations.interface import Interface as IntegrationsInterface


class GitHubPullComments(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "github_pull_comments",
            "description": "get a list of comments from a pull request in GitHub via the GitHub API",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "The owner of the repo - only use if owner is known"
                    },
                    "repo": {
                        "type": "string",
                        "description": "The repository name - only use if the repo is known"
                    },
                    "pull_number": {
                        "type": "number",
                        "description": "The pull request number"
                    }
                },
                "required": ["pull_number"],
            }
        }

    def required_arguments(cls):
        return ["pull_number"]
    
    @classmethod
    def is_system(cls):
        return True
    
    @classmethod
    def parse_fields(cls):
        return {
            "diff_hunk": None,
            "commit_id": None,
            "original_commit_id": None,
            "path": None,
            "body": None,
            "line": None,
            "side": None,
            "position": None
        }

    @classmethod
    def run(cls, arguments, user):
        config = IntegrationsInterface.get_config(user=user, integration_identifier='github')
        if config is None:
            raise Exception("You need to configure the github integration first")
        
        access_token = config['api_key']

        owner = arguments.get('owner') or config.get('owner')
        if owner is None:
            raise Exception('You need to specify an owner')

        repo = arguments.get('repo') or config.get('repo')
        if repo is None:
            raise Exception('You need to specify a repo')
        
        pull_number = arguments['pull_number']

        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments"

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + access_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }

        response = requests.get(
            url,
            headers=headers,
        )

        json = response.json()
        if response.status_code == 200:
            json = [cls.parse_json(comment, cls.parse_fields()) for comment in json]

        print('*'*50)
        print('GitHub response')
        print(response.json())
        print('Parsed response')
        print(json)

        return json
