from django.test import TestCase
from .interface import Interface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder
from unittest.mock import patch
from .response_parsers.gabe import Gabe
from .prompts.interface import Interface as PromptInterface

# Create your tests here.
class LineTest(TestCase):
    # def test_parsing(self):
    #     dict =  {"id": "chatcmpl-7EU6M7Mg9x5ryEEImZSJxbeezHOWg", "model": "gpt-4-0314", "usage": {"total_tokens": 2435, "prompt_tokens": 1894, "completion_tokens": 541}, "object": "chat.completion", "choices": [{"index": 0, "message": {"role": "assistant", "content": "COMMAND: write_file\nARGUMENTS:\n    file_path: \"mysite/urls.py\"\n    content: \"from django.contrib import admin\\nfrom django.urls import path\\nfrom app.views import home, signup, login_view\\n\\nurlpatterns = [\\n    path('', home, name='home'),\\n    path('admin/', admin.site.urls),\\n    path('signup/', signup, name='signup'),\\n    path('login/', login_view, name='login'),\\n    path('api/v1/coder', CreateCoderView.as_view(), name=\\\"create_coder\\\"),\\n    path('api/v1/coder/run', RunCoderView.as_view(), name=\\\"run_coder\\\"),\\n    path('api/v1/coder/append_output', AppendOutputView.as_view(), name=\\\"append_output\\\"),\\n    path('api/v1/coder/user_message', CreateUserMessageView.as_view(), name=\\\"user_message\\\"),\\n    path('api/v1/coder/list', ListCoderView.as_view(), name=\\\"append_output\\\"),\\n    path('api/v1/coder/append_exception', AppendExceptionView.as_view(), name=\\\"append_exception\\\"),\\n    path('api/v1/planner', CreatePlannerView.as_view(), name=\\\"create_planner\\\"),\\n    path('api/v1/planner/run', RunPlannerView.as_view(), name=\\\"run_planner\\\"),\\n    path('api/v1/planner/respond', RespondPlannerView.as_view(), name=\\\"respond_planner\\\"),\\n    path('api/v1/planner/list', ListPlannerView.as_view(), name=\\\"list_planner\\\"),\\n    path('api/v1/planner/generate_tasks', GenerateTaskView.as_view(), name=\\\"generate_tasks\\\"),\\n    path('api/v1/planner/list_tasks', ListTasksView.as_view(), name=\\\"list_tasks\\\"),\\n    path('api/v1/planner/get_messages', GetMessagesView.as_view(), name=\\\"get_messages\\\"),\\n]\\n\"\nEXPLANATION: I will add the `signup` and `login_view` imports from app/views.py, and then add the new URL patterns for 'signup/' and 'login/' from app/urls.py to mysite/urls.py.\nSUMMARY: I've read the content of app/urls.py and mysite/urls.py, and now I'm adding the URLs from app/urls.py to mysite/urls.py.\nTASK: add all urls from app/urls.py to mysite/urls.py\nCOMPLETE: true"}, "finish_reason": "stop"}], "created": 1683686658}
    #     content = dict["choices"][0]["message"]["content"]
    #     parsed = Line.parse_object_to_dict(content)
    #     breakpoint()
    #     with open("test-urls.py", "w") as file:
    #         file.write(parsed["arguments"]["content"])

    def test_parsing(self):
        content = """
        COMMAND: write_file
        ARGUMENTS:
            file_path: Gemfile
            content: source 'https://rubygems.org'\ngit_source(:github) { |repo| "https://github.com/#{repo}.git" }\n\nruby '3.0.3'\n\n# Bundle edge Rails instead: gem 'rails', github: 'rails/rails', branch: 'main'\ngem 'rails', '~> 6.1.4', '>= 6.1.4.1'\n# Use postgresql as the database for Active Record\ngem 'pg', '~> 1.1'\n# Use Puma as the app server\ngem 'puma', '~> 5.0'\n# Use SCSS for stylesheets\ngem 'sass-rails', '>= 6'\n# Transpile app-like JavaScript. Read more: https://github.com/rails/webpacker\n
        gem 'webpacker', '~> 5.0'\n# Turbolinks makes navigating your web application faster. Read more: https://github.com/turbolinks/turbolinks\ngem 'turbolinks', '~> 5'\n# Build JSON APIs with ease. Read more: https://github.com/rails/jbuilder\ngem 'jbuilder', '~> 2.7'\n# Use Redis adapter to run Action Cable in production\ngem 'redis', '~> 4.0'\n# Use Active Model has_secure_password\n
        gem 'bcrypt', '~> 3.1.7'\n\n# Use Active Storage variant\ngem 'image_processing', '~> 1.2'\n\n# Reduces boot times through caching; required in config/boot.rb\ngem 'bootsnap', '>= 1.4.4', require: false\n\ngroup :development, :test do\n  # Call 'byebug' anywhere in the code to stop execution and get a debugger console\n  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]\nend\n\n
        group :development do\n  # Access an interactive console on exception pages or by calling 'console' anywhere in the
        code.\n  gem 'web-console', '>= 4.1.0'\n  gem 'listen', '~> 3.3'\njem 'spring'\n  gem 'spring-watcher-listen', '~> 2.0.0'\nend\n\ngroup :test do\n  # Adds support for Capybara system testing and selenium driver\ngem 'capybara', '>= 3.26'\n  gem 'selenium-webdriver'\n  # Easy installation and use of web drivers to run system tests with browsers\n  gem 'webdrivers'\nend\n\ngem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]\ngem 'devise'\n
        EXPLANATION: Adding the devise gem to the Gemfile
        SUMMARY: Added devise gem to Gemfile
        TASK: add devise to gemfile
        COMPLETE: true
        """

        PromptInterface("2").parse(content)


    # def test_gabe_parsing(self):
    #     response = """
    #     READ,GEMFILE
    #     """
    #     # Gabe().parse_response(response)

    # def test_no_command_response(self):
    #     response = "Great! I have successfully added the Devise gem to the Gemfile. If you have any more tasks or questions, feel free to ask."
    #     parsed = Gabe().parse_response(response)
    #     self.assertEqual(parsed, { "comment": response })

    # def test_with_command(self):
    #     response = "My apologies for the formatting error. Let me add the Devise gem to the Gemfile correctly.\n\nUPDATE,Gemfile\nsource \"https://rubygems.org\"\ngit_source(:github) { |repo| \"https://github.com/#{repo}.git\" }\n\nruby \"3.1.2\"\n\ngem \"rails\", \"~> 7.0.4\", \">= 7.0.4.3\"\ngem \"sprockets-rails\"\ngem \"sqlite3\", \"~> 1.4\"\ngem \"puma\", \"~> 5.0\"\ngem \"importmap-rails\"\ngem \"turbo-rails\"\ngem \"stimulus-rails\"\ngem \"jbuilder\"\ngem \"redis\", \"~> 4.0\"\ngem \"tzinfo-data\", platforms: %i[ mingw mswin x64_mingw jruby ]\ngem \"bootsnap\", require: false\n\ngroup :development, :test do\n  gem \"debug\", platforms: %i[ mri mingw x64_mingw ]\nend\n\ngroup :development do\n  gem \"web-console\"\nend\n\ngroup :test do\n  gem \"capybara\"\n  gem \"selenium-webdriver\"\n  gem \"webdrivers\"\nend\n\ngem \"bootstrap\", \"~> 5.1\"\ngem \"devise\"\n\nNow the Devise gem is added to the Gemfile."
    #     parsed = Gabe().parse_response(response)
    #     self.assertEqual(parsed["comment"], "My apologies for the formatting error. Let me add the Devise gem to the Gemfile correctly.\n\n")
    #     self.assertEqual(parsed["command"], 'write_file')
    #     self.assertEqual(parsed["arguments"]["file_path"], "Gemfile")


# class InterfaceTest(TestCase):
#     def setUp(self):
#         self.coder = Interface.create_coder(
#             tasks=["task 1", "task 2"],
#             requirements="These are my requirements",
#             context="This is the context",
#             description="Test description"
#         )

#     def test_creation(self):
#         self.assertEqual(self.coder.tasks, ["task 1", "task 2"])
#         self.assertEqual(self.coder.requirements, "These are my requirements")
#         self.assertEqual(self.coder.context, "This is the context")
#         self.assertEqual(self.coder.current_task_index, 0)
#         self.assertEqual(self.coder.files_changed, {})
#         self.assertEqual(self.coder.complete, False)
#         self.assertEqual(self.coder.description, "Test description")

#         messages = MessagesInterface(Coder, self.coder.id).list()
#         self.assertEqual(messages[0].message_content["role"], "system")
#         self.assertEqual(messages[1].message_content["task"], True)

#     def test_api_methods(self):
#         interface = Interface(self.coder.id)
#         self.assertEqual(interface.current_command(), None)
#         # with an invalid response
#         with patch.object(Interface, '_Interface__run_completion', return_value="{}") as mock_method:
#             interface.run()
#         messages = MessagesInterface(Coder, self.coder.id).list()
#         self.assertEqual(len(messages), 4)
#         self.assertEqual(messages[-2].message_content, { "content": "{}", "role": "assistant", "error": True, "task": False })
#         self.assertEqual(messages[-1].message_content, { "content": "Could not parse your response due to:\nCould not find the command\nPlease try again following the response format", "role": "user", "error": True, "task": False })
#         self.assertEqual(interface.current_command(), None)
#         valid_response = "{\"command\":\"create_file\",\"arguments\":{\"file_path\":\"test.py\"},\"explanation\":\"testing\",\"summary\":\"running tests\",\"task\":\"task 1\",\"complete\":false}" 
#         with patch.object(Interface, '_Interface__run_completion', return_value=valid_response) as mock_method:
#             interface.run()
#         messages = MessagesInterface(Coder, self.coder.id).list()
#         self.assertEqual(len(messages), 5)
#         self.assertEqual(interface.current_command(), {
#             "command": "create_file",
#             "arguments": { "file_path": "test.py" },
#             "explanation": "testing",
#             "summary": "running tests",
#             "task": "task 1",
#             "complete": False
#         })
#         interface.append_output("command executed successfully")
#         messages = MessagesInterface(Coder, self.coder.id).list()
#         self.assertEqual(len(messages), 6)
#         self.assertEqual(self.coder.current_task_index, 0)
#         task_complete_response = "{\"command\":\"create_file\",\"arguments\":{\"file_path\":\"test.py\"},\"explanation\":\"testing\",\"summary\":\"running tests\",\"task\":\"task 1\",\"complete\":true}" 
#         with patch.object(Interface, '_Interface__run_completion', return_value=task_complete_response) as mock_method:
#             interface.run()
#         interface.append_output("command executed successfully")
#         messages = MessagesInterface(Coder, self.coder.id).list()
#         self.assertEqual(len(messages), 9)
#         self.coder.refresh_from_db()
#         self.assertEqual(self.coder.current_task_index, 1)
#         invalid_argument_response = "{\"command\":\"create_file\",\"arguments\":{\"invalid\":\"test.py\"},\"explanation\":\"testing\",\"summary\":\"running tests\",\"task\":\"task 1\",\"complete\":false}" 
#         with patch.object(Interface, '_Interface__run_completion', return_value=invalid_argument_response) as mock_method:
#             interface.run()
#         messages = MessagesInterface(Coder, self.coder.id).list()
#         self.assertEqual(len(messages), 11)
#         self.assertEqual(messages[-1].message_content, { "content": "The arguments you provided had validation errors:\n{'file_path': ['missing']}\nPlease try again with the proper arguments", "role": "user", "error": True, "task": False})