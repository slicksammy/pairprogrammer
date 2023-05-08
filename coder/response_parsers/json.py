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

        Escape all quotes with a backslash, for example:
        {
            "command": "write_file",
            "arguments": {
                "content": "\"\"\" some content \"\"\""
            },
            "explanation": "I need to create a new file",
            "summary": "creating a file",
            "task": "the task you are working on",
            "complete": false
        }
        """
    
    @classmethod
    def parse_response_object(cls, response):
        return response
    
    @classmethod
    def parse_object_to_dict(cls, object):
        return json.loads(object)