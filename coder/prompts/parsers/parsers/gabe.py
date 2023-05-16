import textwrap
import re
class Gabe:
    def __init__(self):
        self.available_commands = [
            "QUESTION",
            "READ",
            "CREATE",
            "UPDATE",
            "RAILS",
            "BUNDLE",
            # "YARN"
        ]

    def resposne_format_prompt(self):
        command_prompts = map(lambda command: self.__build_command_prompt(command), self.available_commands)
        prompt = "\n".join(command_prompts)

        return textwrap.dedent(f"""
        RESPOND WITH ONE OF THE FOLLOWING FORMATS:

         {prompt}
        """).strip()
    
    def parse_response(self, response):
        response = response.strip()
        piped_commands = "|".join(self.available_commands)
        if not re.search(fr'{piped_commands}', response, re.DOTALL):
            # no command
            return { "comment": response }
        pattern = fr'^(.*?)({piped_commands}),(.*?$.*?)$'
        match = re.search(pattern, response, re.DOTALL)
        comment = match.group(1)  # Everything before the keyword
        command = match.group(2)  # The keyword (READ, WRITE, or BUNDLE)
        arguments = match.group(3)
        if command == "QUESTION":
            command = {
                "command": "ask_question",
                "arguments": {
                    "question": arguments
                }
            }
        elif command == "READ":
            command = {
                "command": "read_file",
                "arguments": {
                    "file_path": arguments
                }
            }
        elif command == "CREATE":
            command = {
                "command": "read_file",
                "arguments": {
                    "file_path": arguments
                }
            }
        elif command == "BUNDLE":
            command = {
                "command": "bundle",
                "arguments": {
                    "command": arguments
                }
            }
        elif command == "RAILS":
            command = {
                "command": "rails",
                "arguments": {
                    "command": arguments
                }
            }
        elif command == "UPDATE":
            file_path, content = arguments.split('\n', maxsplit=1)
            content = content.strip("`").encode().decode('unicode_escape')
            command = {
                "command": "write_file",
                "arguments": {
                    "file_path": file_path,
                    "content": content
                }
            }

        command.update({ "comment": comment })
        return command

    def __build_command_prompt(self, command):
        if command == "QUESTION":
            prompt = """
            If you need more clarification or want to ask the user a question, use the following FORMAT:
            QUESTION,{question}
            """
        elif command == "READ":
            prompt = """
            If you want to read a file, use the following FORMAT. The output will be given back to you for subsequent tasks:
            READ,{filename}
            """
        elif command == "CREATE":
            prompt = """
            If you want to create a file, use the following FORMAT:
            CREATE,{filename}
            """
        elif command == "UPDATE":
            prompt = """
            If you want to update an existing file, use the following FORMAT
            UPDATE,{filename}
            {new_content}
            But you can only update a file if you already know it's contents.
            """
        elif command == "RAILS":
            prompt = """
            If you want to run a Rails shell command, use the following FORMAT. All Ruby binaries are available:
            RAILS,{cmd}
            """
        elif command == "BUNDLE":
            prompt = """
            If you want to run a Bundler shell command, use the following FORMAT. All Ruby binaries are available:
            BUNDLE,{cmd}
            """
        else:
            raise Exception("Invalid Command")
        
        return textwrap.dedent(prompt).strip()
