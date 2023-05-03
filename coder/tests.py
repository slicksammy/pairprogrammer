from django.test import TestCase
from .interface import Interface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder
from unittest.mock import patch

# Create your tests here.
class InterfaceTest(TestCase):
    def setUp(self):
        self.coder = Interface.create_coder(
            tasks=["task 1", "task 2"],
            requirements="These are my requirements",
            context="This is the context"
        )

    def test_creation(self):
        self.assertEqual(self.coder.tasks, ["task 1", "task 2"])
        self.assertEqual(self.coder.requirements, "These are my requirements")
        self.assertEqual(self.coder.context, "This is the context")
        self.assertEqual(self.coder.current_task_index, 0)
        self.assertEqual(self.coder.files_changed, {})
        self.assertEqual(self.coder.complete, False)

        messages = MessagesInterface(Coder, self.coder.id).list()
        self.assertEqual(messages[0].message_content["role"], "system")
        self.assertEqual(messages[1].message_content["task"], True)

    def test_api_methods(self):
        interface = Interface(self.coder.id)
        self.assertEqual(interface.current_command(), None)
        # with an invalid response
        with patch.object(Interface, '_Interface__run_completion', return_value="Test") as mock_method:
            interface.run()
        messages = MessagesInterface(Coder, self.coder.id).list()
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[-2].message_content, { "content": "Test", "role": "assistant", "error": True, "task": False })
        self.assertEqual(messages[-1].message_content, { "content": "Could not parse your response due to:\nCould not find the command\nPlease try again following the response format", "role": "user", "error": True, "task": False })
        self.assertEqual(interface.current_command(), None)
        valid_response = """
        COMMAND: create_file
        ARGUMENTS: { "file_path": "test.py" }
        EXPLANATION: testing
        SUMMARY: running tests
        TASK: task 1
        COMPLETE: false
        """
        with patch.object(Interface, '_Interface__run_completion', return_value=valid_response) as mock_method:
            interface.run()
        messages = MessagesInterface(Coder, self.coder.id).list()
        self.assertEqual(len(messages), 5)
        self.assertEqual(interface.current_command(), {
            "command": "create_file",
            "arguments": { "file_path": "test.py" },
            "explanation": "testing",
            "summary": "running tests",
            "task": "task 1",
            "complete": False
        })
        interface.append_output("command executed successfully")
        messages = MessagesInterface(Coder, self.coder.id).list()
        self.assertEqual(len(messages), 6)
        self.assertEqual(self.coder.current_task_index, 0)
        task_complete_response = """
        COMMAND: create_file
        ARGUMENTS: { "file_path": "test.py" }
        EXPLANATION: testing
        SUMMARY: running tests
        TASK: task 1
        COMPLETE: true
        """
        with patch.object(Interface, '_Interface__run_completion', return_value=task_complete_response) as mock_method:
            interface.run()
        interface.append_output("command executed successfully")
        messages = MessagesInterface(Coder, self.coder.id).list()
        self.assertEqual(len(messages), 9)
        self.coder.refresh_from_db()
        self.assertEqual(self.coder.current_task_index, 1)
        invalid_argument_response = """
        COMMAND: create_file
        ARGUMENTS: { "something": "test.py" }
        EXPLANATION: testing
        SUMMARY: running tests
        TASK: task 1
        COMPLETE: true
        """
        with patch.object(Interface, '_Interface__run_completion', return_value=invalid_argument_response) as mock_method:
            interface.run()
        messages = MessagesInterface(Coder, self.coder.id).list()
        self.assertEqual(len(messages), 11)
        self.assertEqual(messages[-1].message_content, { "content": "The arguments you provided had validation errors:\n{'file_path': ['missing']}\nPlease try again with the proper arguments", "role": "user", "error": True, "task": False})