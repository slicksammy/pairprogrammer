import json
from json.decoder import JSONDecodeError
import textwrap
from coder.exceptions import InvalidAssistantResponseException

class Json:
    @classmethod
    def prompt(cls):
        return textwrap.dedent("""
        Respond with a ONLY a PYTHON JSON object with the following fields:
        
        "command": create_file (string)
        "arguments": {"file_path": "some/file_path.rb"} (json) // If there are no arguments, use an empty JSON object: {}
        "explanation": I need to create a new file (string)
        "summary": creating a file (string)
        "task": the task you are working on (string)
        "complete": if the current task has been completed (boolean)

        Example:
        {
            "command": "create_file",
            "arguments": {
                "file_path": "some/file_path.rb"
            },
            "explanation": "I need to create a new file",
            "summary": "creating a file",
            "task": "the task you are working on",
            "complete": false
        }
        """).strip()
    
    @classmethod
    def parse_response(cls, response):
        json_string = None
        
        try:
            start_index = response.index("{")  # find the first occurrence of the opening brace
            end_index = response.rindex("}")  # find the last occurrence of the closing brace
            json_string = response[start_index:end_index+1]
        except ValueError:
            return {
                "explanation": response 
            }
        try:
            return json.loads(json_string)
        except JSONDecodeError as e:
            raise InvalidAssistantResponseException(e.args[0])