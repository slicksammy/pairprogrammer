from completions.interface import Interface as CompletionsInterface
class Interface:
    def __init__(self):
        pass

    def fix_file(self, file_path, file_contents, model="gpt-4"):
        content = self.__create_prompt(file_path, file_contents)
        completions_interface = CompletionsInterface()
        new_file_contents = completions_interface.run_completion([{ "role": "user", "content": content }], model)
        lines = new_file_contents.split("\n")
        if lines[0].startswith("```"):
            lines.pop(0)
        if lines[-1].startswith("```"):
            lines.pop
        return "\n".join(lines)
    
    def __create_prompt(self, file_path, file_contents):
        return "\n".join([f"This is file {file_path} and here are the contents", file_contents, "Cleanup any syntax errors and return just the updated file contents, no additional characters"])