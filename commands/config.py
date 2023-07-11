from commands.commands import *

class Config:
    COMMAND_GROUPS = {
        "coding": {"display": "Coding", "description": "Reads, write, and runs commands on your local system"},
        "memory": {"display": "Memory", "description": "Commands to help you remember and recall things"},
        "honeybadger": {"display": "Honeybadger", "description": "Commands to interact with Honeybadger"},
        "github": {"display": "Github", "description": "Commands to interact with Github"},
        "railway": {"display": "Railway", "description": "Commands to interact with Railway"}
    }

    COMMANDS = {
        "delete_file": {"command_class": DeleteFile, "display": "Delete File", "description": "Command to delete a file.", "group": COMMAND_GROUPS["coding"]},
        "view_changes": {"command_class": ViewChanges, "display": "View Changes", "description": "Command to view changes.", "group": COMMAND_GROUPS["coding"]},
        "delete_lines": {"command_class": DeleteLines, "display": "Delete Lines", "description": "Command to delete lines.", "group": COMMAND_GROUPS["coding"]},
        "rspec": {"command_class": Rspec, "display": "Run Rspec", "description": "Command to run Rspec tests.", "group": COMMAND_GROUPS["coding"]},
        "read_file": {"command_class": ReadFile, "display": "Read File", "description": "Command to read a file.", "group": COMMAND_GROUPS["coding"]},
        "create_file": {"command_class": CreateFile, "display": "Create File", "description": "Command to create a file.", "group": COMMAND_GROUPS["coding"]},
        "create_directory": {"command_class": CreateDirectory, "display": "Create Directory", "description": "Command to create a directory.", "group": COMMAND_GROUPS["coding"]},
        "comment": {"command_class": Comment, "display": "Add a Comment", "description": "Command to add a comment.", "group": None},
        "write_file": {"command_class": WriteFile, "display": "Write to a File", "description": "Command to write to a file.", "group": COMMAND_GROUPS["coding"]},
        "rails": {"command_class": Rails, "display": "Execute Rails Command", "description": "Command to execute a Rails command.", "group": COMMAND_GROUPS["coding"]},
        "bundle": {"command_class": Bundle, "display": "Execute Bundle", "description": "Command to execute a Bundle command.", "group": COMMAND_GROUPS["coding"]},
        "ls": {"command_class": Ls, "display": "List Directory", "description": "Command to list items in a directory.", "group": COMMAND_GROUPS["coding"]},
        "python": {"command_class": Python, "display": "Execute Python Command", "description": "Command to execute a Python command.", "group": COMMAND_GROUPS["coding"]},
        "mv": {"command_class": Mv, "display": "Move or Rename Files", "description": "Command to move or rename files.", "group": COMMAND_GROUPS["coding"]},
        "yarn": {"command_class": Yarn, "display": "Execute Yarn Command", "description": "Command to execute a Yarn command.", "group": COMMAND_GROUPS["coding"]},
        "recall": {"command_class": Recall, "display": "Recall Memory", "description": "Command to recall a memory.", "group": COMMAND_GROUPS["memory"]},
        "remember": {"command_class": Remember, "display": "Remember Information", "description": "Command to remember information.", "group": COMMAND_GROUPS["memory"]},
        "honey_badger_fault_list": {"command_class": HoneyBadgerFaultList, "display": "HoneyBadger Fault List", "description": "Command to list HoneyBadger faults.", "group": COMMAND_GROUPS["honeybadger"]},
        "honey_badger_fault_id": {"command_class": HoneyBadgerFaultID, "display": "HoneyBadger Fault ID", "description": "Command to get a fault by id from the HoneyBadger.", "group": COMMAND_GROUPS["honeybadger"]},
        "list_github_pull_request": {"command_class": ListGitHubPullRequest, "display": "List Pull Requests", "description": "Command to create a pull request on GitHub.", "group": COMMAND_GROUPS["github"]},
        "github_pull_comments": {"command_class": GitHubPullComments, "display": "Pull Request Comments", "description": "Command to retrieve comments on pull request.", "group": COMMAND_GROUPS["github"]},
        "github_pull_comment_replies": {"command_class": GitHubPullCommentReplies, "display": "Reply to Pull Request Comment", "description": "Command to reply to a comment on pull request.", "group": COMMAND_GROUPS["github"]},
        "railway_get_information": {"command_class": RailwayGetInformation, "display": "Get Railway Project Information", "description": "Command to retrieve information about a Railway project.", "group": COMMAND_GROUPS["railway"]}
    }
    
    @classmethod
    def get_command(cls, command):
        return cls.COMMANDS[command]

    @classmethod
    def command_exists(cls, command):
        return command in cls.COMMANDS
