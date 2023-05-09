import json

class Json:
    @classmethod
    def response_prompt(cls):
        return """
        Respond with a ONLY a JSON object with the following fields:
        
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

        Escape the following characters with a single backslash:
            - Double quote (`"`) eg \"
            - Backslash (`\`) eg \\
            - Controler characters
                - Tab `\t` eg \\t
                - Newline `\n` eg \\n
                - Carriage return `\r` eg \\n
        """
    
    @classmethod
    def parse_response_object(cls, response):
        start_index = response.index("{")  # find the first occurrence of the opening brace
        end_index = response.rindex("}")  # find the last occurrence of the closing brace
        return response[start_index:end_index+1]
    
    @classmethod
    def parse_object_to_dict(cls, object):
        return json.loads(object)