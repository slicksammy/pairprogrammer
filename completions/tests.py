from django.contrib.auth.models import User
from django.test import TestCase
from completions.models import Completion
from completions.interface import Interface
from unittest.mock import patch, Mock
import openai
import uuid

class CreateCompletionTestCase(TestCase):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()

        self.mock_func = patch.object(openai.ChatCompletion, 'create', return_value={"choices": [{'message': {'content': 'test'}}]})
        self.mock_func.start()

    def tearDown(self):
        self.mock_func.stop()
        super().tearDown()

    def test_create_completion(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
        model = "gpt-4-0613"
        completion = Interface.create_completion(self.user, 'use_case', messages, model)
        
        self.assertIsInstance(completion, Completion)
        self.assertIsNotNone(completion.id)
        self.assertIsNotNone(completion.message)
        self.assertEqual(completion.message, {'content': 'test'})