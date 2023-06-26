from coder.exceptions import InvalidArgumentsException
import textwrap

class Line:
    def __init__(self):
        pass

    @classmethod
    def prompt(self):
        return textwrap.dedent("""
        Use the following format for your response:
                
        COMMAND: one of the commands you have
        ARGUMENTS:
            ARGUMENT_1: ...
            ARGUMENT_2: ...
        EXPLANATION: Why you are running this command
        SUMMARY: What you have done so far
        TASK: which task you are working on
        COMPLETE: if the current task has been completed (true/false)
        
        All fields are required
        """)
    
    @classmethod
    def parse_response(self, response):
        lines = response.split('\n')
        lines = [line.strip() for line in lines]
        parsed = {}

        for i in range(len(lines)):
            if lines[i].startswith('COMMAND:'):
                parsed['command'] = lines[i].split('COMMAND: ')[1].strip()
            elif lines[i].startswith('ARGUMENTS:'):
                arguments = {}
                i += 1
                while i < len(lines) and not lines[i].startswith('EXPLANATION:'):
                    key, value = lines[i].split(': ', maxsplit=1)
                    arguments[key.strip()] = value.strip().strip('"').strip("`").encode().decode('unicode_escape') #.strip("'").replace("\\n", "\n") # because linebreaks are separators, the api will return \\n indicating it to not be a line break
                    i += 1
                parsed["arguments"] = arguments
            elif lines[i].startswith('EXPLANATION:'):
                parsed['explanation'] = lines[i].split('EXPLANATION: ')[1].strip()
            elif lines[i].startswith('SUMMARY:'):
                parsed['summary'] = lines[i].split('SUMMARY: ')[1].strip()
            elif lines[i].startswith('TASK:'):
                parsed['task'] = lines[i].split('TASK: ')[1].strip()
            elif lines[i].startswith('COMPLETE:'):
                parsed['complete'] = lines[i].split('COMPLETE: ')[1].strip().lower() == 'true'
        
        return parsed