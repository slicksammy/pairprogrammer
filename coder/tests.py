from django.test import TestCase
from .interface import Interface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder
from unittest.mock import patch, MagicMock
from .prompts.interface import Interface as PromptInterface
from django.contrib.auth.models import User


class TestRunFunction(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

    @patch('coder.interface.Interface._Interface__run_completion')
    def test_run_function(self, mock_run_completion):
        # Create a test coder
        test_coder = Coder.objects.create(
            tasks=['test task'],
            requirements=['test requirement'],
            context='test context',
            current_task_index=0,
            complete=False,
            user_id=self.test_user.id
        )

        # Define the mock value for __run_completion
        mock_completion = MagicMock()
        mock_completion.content.return_value = '{"command": "create_file", "arguments": {"file_path": "some/file_path.rb"}, "explanation": "I need to create a new file", "summary": "creating a file", "task": "the task you are working on", "complete": false}'
        mock_run_completion.return_value = mock_completion

        # Create Interface instance with the test coder
        interface_instance = Interface(test_coder.id)

        # Call the run function
        interface_instance.run()

        # Check if the run function executed successfully
        self.assertNotEqual(interface_instance.status()['running'], True)
        mock_run_completion.assert_called_once()


# Create your tests here.
