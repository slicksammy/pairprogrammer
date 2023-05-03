from django.test import TestCase
from .interface import Interface
# Create your tests here.
class InterfaceTest(TestCase):
    def test_success_validations(self):
        validations = Interface.validate_arguments("create_file", { "file_path": "test" })
        self.assertEqual(validations, {})

    def test_fail_validations(self):
        validations = Interface.validate_arguments("create_file", {})
        self.assertEqual(validations, { "file_path": ["missing"] })

    def test_custom_validations(self):
        validations = Interface.validate_arguments("delete_lines", { "file_path": "test", "line_numbers": [] })
        self.assertEqual(validations, { "line_numbers": ["must include at least one line number"] })