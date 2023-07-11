from .base import Base
import requests
from django.conf import settings
from commands.helpers import is_relative
from integrations.interface import Interface as IntegrationsInterface


class GitHubPullCommentReplies(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "github_pull_comment_replies",
            "description": "reply to a comment from a pull request in GitHub via the GitHub API",
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
                    },
                    "comment_id": {
                        "type": "number",
                        "description": "The comment ID number"
                    },
                    "body": {
                        "type": "string",
                        "description": "The body of the reply"
                    }
                },
                "required": ["pull_number", "comment_id", "body"],
            }
        }

    def required_arguments(cls):
        return ["pull_number", "comment_id", "body", "repo", "owner"]
    
    @classmethod
    def is_system(cls):
        return True
    
    @classmethod
    def run(cls, arguments, user):
        access_token = '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'
        owner = arguments.get('owner')
        repo = arguments.get('repo')
        pull_number = arguments['pull_number']

        comment_id = arguments['comment_id']

        body = arguments['body']

        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies"

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + access_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }

        data = {
            'body': body
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
        )

        json = response.json()
        if response.status_code == 200:
            json = "Comment saved"

        print('*'*50)
        print('GitHub response')
        print(response.json())
        print('Parsed response')
        print(json)

        return json
