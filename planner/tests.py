from django.test import TestCase
from .interface import Interface
from app_messages.interface import Interface as MessagesInterface
from .models import Planner
# Create your tests here.
class InterfaceTest(TestCase):
    def setUp(self):
        self.planner = Interface.create_planner(
            requirements="requirements",
            context="context",
            description="description"
        )

    def test_creation(self):
        self.assertEqual(self.planner.requirements, "requirements")
        self.assertEqual(self.planner.context, "context")
        self.assertEqual(self.planner.description, "description")
        self.assertEqual(self.planner.tasks, [])

        messages = MessagesInterface(Planner, self.planner.id).list()
        self.assertEqual(messages[0].message_content["role"], "system")
        self.assertEqual(len(messages), 1)
        interface = Interface(self.planner.id)
        self.assertEqual(interface.get_tasks(), [])
        self.assertEqual(len(interface.get_messages()), 1)