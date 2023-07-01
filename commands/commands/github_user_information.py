import requests
from .base import Base
from commands.helpers import is_relative

class GithubUserInformation(Base):
    @classmethod
    def schema(cls):
        return {
            "name": "github_user_information",
            "description": "Get information on the user including their username",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }

    def required_arguments(cls):
        return []
    
    @classmethod
    def run(self, arguments, user):
        AUTH_TOKEN = 'YOUR_GITHUB_PERSONAL_ACCESS_TOKEN'
        url = "https://api.github.com/user"

        headers = { 'Authorization': f'Bearer {AUTH_TOKEN}', "X-GitHub-Api-Version": "2022-11-28", "Accept": "Accept: application/vnd.github+json" }

        response = requests.get(
            url,
            headers=headers,
        )

        print("*"*50)
        print("GitHub PR response")
        print(response.json())
        
        if response.status_code == 200:
            return {
                "username": response.json().get("login")
            }
        else:
            return response.json()