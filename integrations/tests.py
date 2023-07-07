import json
from django.test import TestCase
from .interface import Interface
from .models import Integration
from django.contrib.auth.models import User


class InterfaceTestCase(TestCase):
    
    def setUp(self):
        self.valid_config = {"api_key": "123", "project_id": "45", "description": "test"}
        self.user = User.objects.create(username="test")

    def test_create_integration(self):
        Interface.create_integration("honeybadger", self.user, self.valid_config)
        integration = Integration.objects.get(user=self.user)

        self.assertEqual(integration.integration, "honeybadger")
        self.assertEqual(integration.config, self.valid_config)
