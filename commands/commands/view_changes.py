from .base import Base
import subprocess

class ViewChanges(Base):
    @classmethod
    def required_arguments(cls):
        return []
    
    def execute(self, created_files, updated_files, deleted_files):
        diff = []

        if len(self.created_files) > 0:
            diff.append("CREATED FILES:")
            diff.extend([f"File: {file_path}\n{open(file_path).read()}\n" for file_path in created_files])
            diff.append("\n")

        if len(self.updated_files) > 0:
            diff.append("UPDATED FILES:")
            diff.extend([f'File: {file_path}\n{subprocess.check_output(["git", "diff", file_path], universal_newlines=True)}\n' for file_path in updated_files])
            diff.append("\n")

        if len(self.deleted_files) > 0:
            diff.append("DELETED FILES:")
            diff.extend([f"File: {file_path}\n" for file_path in deleted_files])

        return "\n".join(diff)
        