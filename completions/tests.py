from django.test import TestCase
from completions.models import Completion
from completions.interface import Interface
from unittest.mock import patch
import openai
import uuid
from coder.models import Coder


class CreateCompletionTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.mock_func = patch.object(openai.ChatCompletion, 'create', return_value={"choices": [{"message": {"content": "test"}}]})
        self.mock_func.start()
        self.coder = Coder.objects.create(
            tasks=[],
            requirements='requirements',
            context='context',
            current_task_index=0,
            complete=False,
        )

    def tearDown(self):
        self.mock_func.stop()
        super().tearDown()

    def test_create_completion(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
        model = "gpt-3.5-turbo"
        completion = Interface.create_completion(completer_type=Coder, completer_id=self.coder.id, messages=messages, model=model)
        self.assertIsInstance(completion, Completion)
        self.assertIsNotNone(completion.id)
        self.assertIsNotNone(completion.content)
        self.assertEqual(completion.content, "test")

# Create your tests here.
