from django.utils import timezone
from coder.exceptions import InvalidAssistantResponseException, NotEnoughTokensException
from commands.interface import Interface as CommandInterface
from completions.interface import Interface as CompletionsInterface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder, CoderMessage
import textwrap
from planner.interface import Interface as PlannerInterface
from coder.prompts.interface import Interface as PromptInterface
from .prompts.interface import Interface as PromptInterface
from app.models import User
from openai.error import OpenAIError
from .recipes.original import Original as OriginalRecipe
from .recipes.function_call import FunctionCall as FunctionCallRecipe
import traceback

class Interface:
    @classmethod
    def create_coder_from_planner(cls, planner_id):
        planner_inteface = PlannerInterface(planner_id)
        planner = planner_inteface.planner
        tasks = planner.tasks
        requirements = planner.requirements
        context = planner.context
        return cls.create_coder(tasks, requirements, context)
        

    @classmethod
    def create_coder(cls, tasks, requirements, context, user_id, prompt_version="1"):
        coder = Coder.objects.create(
            tasks=tasks,
            requirements=requirements,
            context=context,
            current_task_index=0,
            complete=False,
            user_id=user_id
        )

        FunctionCallRecipe(coder).after_create()

        return coder

    # created
    # running + running_at
    # completion_api_error # when model call fails
    # command_error # no command, invalid command, invalid command arguments
    # command_success
    # user_input
    # command_output
    # unknown_error
    # completed
    def run(self):
        if self.coder.running_at is not None:
            pass
        
        if self.coder.reached_max_length:
            return

        latest_message = CoderMessage.objects.filter(coder=self.coder).order_by('-created_at').first()
        # command was successful, awaiting a response
        if latest_message is not None and latest_message.command_error is None and latest_message.command is not None:
            return
        
        self.coder.running_at = timezone.now()
        self.coder.error = None
        self.coder.save()
        
        try:
            self.recipe(self.coder).before_run(latest_message)
            
            completion = self.recipe(self.coder).on_run()
            if completion.context_length_exceeded:
                self.coder.error = {
                    "code": "reached_max_length"
                }
                self.coder.reached_max_length = True
                self.coder.running_at = None
                self.coder.save()
                return
            elif completion.error:
                self.coder.error =  {
                    "code": "completion_api_error"
                }
                self.coder.running_at = None
                self.coder.save()
                return
            

            message = self.recipe(self.coder).get_completion_message(completion)
            command = self.recipe(self.coder).parse_command_from_message(message)

            if command is None:
                CoderMessage.objects.create(
                    coder = self.coder,
                    role = message["role"],
                    function_name = message.get("name"),
                    content = message.get("content"),
                    function_call = message.get("function_call"),
                    command = command,
                    command_error = {
                        "code": "missing_command"
                    }
                )
                self.coder.error = {
                    "code": "missing_command"
                }
            else:
                the_command = command.get("command")
                command_exists = CommandInterface.command_exists(the_command)
                if not command_exists:
                    CoderMessage.objects.create(
                        coder = self.coder,
                        role = message["role"],
                        function_name = message.get("name"),
                        content = message.get("content"),
                        function_call = message.get("function_call"),
                        command = command,
                        command_error = {
                            "code": "invalid_command"
                        }
                    )
                    self.coder.error = {
                        "code": "invalid_command"
                    }
                else:
                    arguments = command.get("arguments")
                    argument_validations = CommandInterface.validate_arguments(the_command, arguments)
                    if len(argument_validations) > 0:
                        CoderMessage.objects.create(
                            coder = self.coder,
                            role = message["role"],
                            function_name = message.get("name"),
                            content = message.get("content"),
                            function_call = message.get("function_call"),
                            command = command,
                            command_error = {
                                "code": "invalid_arguments",
                                "validation_errors": argument_validations
                            }
                        )
                        self.coder.error = {
                            "code": "invalid_arguments"
                        }
                    else:
                        CoderMessage.objects.create(
                            coder = self.coder,
                            role = message["role"],
                            function_name = message.get("name"),
                            content = message.get("content"),
                            function_call = message.get("function_call"),
                            command = command,
                            command_error = None
                        )

        except Exception as e:
            breakpoint()
            self.coder.error = {
                "code": "unknown"
            }
        finally:
            self.coder.running_at = None
            self.coder.save()

    

    @classmethod
    def list(cls, user_id):
        return list(map(lambda coder: { "id" : coder.id, "tasks": coder.tasks, "requirements": coder.requirements, "created_at": coder.created_at }, list(Coder.objects.filter(user_id=user_id).order_by("-created_at").all())))

    def __init__(self, coder_id):
        self.coder = Coder.objects.get(id=coder_id)
        self.version = "1"
        self.model = "gpt-4"
        self.recipe = FunctionCallRecipe

    # TODO update this
    def display_messages(self):
        for message in self.messages:
            print(message.message_content["role"])
            print(message.message_content["content"])
            if message.message_content.get("parsed") is not None:
                print(message.message_content["parsed"])
            print(message.message_content["error"])

    def append_output(self, output, command):
        latest_command_message = CoderMessage.objects.filter(coder=self.coder, command__isnull=False, command_error__isnull=True).latest('created_at')
        # latest command message is getting passed here because first the user submits the otuput then we can check if the original task was completed
        self.recipe(self.coder).on_function_call(output, command, latest_command_message)

    def append_user_message(self, content):
        CoderMessage.objects.create(
            coder=self.coder,
            role="user",
            function_name=None,
            content=content,
            function_call=None
        )
    
    def status(self):
        if self.coder.running_at:
            return {
                "running": True,
                "running_at": self.coder.running_at,
            }
        else:
            latest_message = CoderMessage.objects.filter(coder=self.coder).order_by('-created_at').first()

            return {
                "running": False,
                "error": self.coder.error is not None,
                "system_message": latest_message.command if latest_message.command_error is None else None,
                "reached_max_length": self.coder.reached_max_length,
                "availabe_tokens": 1000 #CompletionsInterface.available_completion_tokens(self.messages, self.model)
            }

    # this message we send back to the client until we receive a response
    # def __current_assistant_message(self):
    #     if (self.messages[-1].message_content["role"] == "assistant") and not(self.messages[-1].message_content["error"]):
    #         return self.messages[-1].message_content["parsed"]
        
    # def __last_assistant_message(self):
    #     return next((message for message in reversed(self.messages) if message.message_content.get("role") == "assistant"), None)

    # def current_task(self):
    #     return self.coder.tasks[self.coder.current_task_index]
    
    # def complete(self):
    #     return self.coder.complete

    # def skip_task(self):
    #     self.__next_task()

    def client_error(self, exception_class, exception_message):
        CoderMessage.objects.create(
            coder=self.coder,
            role="user",
            function_name=None,
            content=f'unexpected exception {exception_class} {exception_message}',
            function_call=None
        )

    # def __log(self, name, content):
    #     print("*"*50)
    #     print(name)
    #     print(content)
    #     print("*"*50)

    # def __append_response_exception(self, e):
    #     content = textwrap.dedent(f"""
    #     Could not parse your response due to:
    #     {e.args[0]}
    #     Please try again following the response format
    #     """).strip()
        
    #     self.__append_message(content, role="user", error=True)

    # def __append_invalid_command(self, command):
    #     content = textwrap.dedent(f"""
    #     {command} is not a valid command
    #     """).strip()
        
    #     self.__append_message(content, role="user")

    # def __append_argument_validations(self, validation_errors):
    #     content = textwrap.dedent(f"""
    #     The arguments you provided have the following validation errors:
    #     {validation_errors}
    #     Please try again with the proper arguments
    #     """).strip()
        
    #     self.__append_message(content, role="user")

    # def __mark_previous_message_as_error(self):
    #     message = self.messages[-1]
    #     message.message_content["error"] = True
    #     # TODO this should be in the messages interface
    #     message.save()

    # # TODO configure model on coder instance
    # def __run_completion(self, model):
    #     formatted_messages = [{ "content": message.message_content["content"], "role": message.message_content["role"] } for message in self.messages]
    #     # TODO rescue openai.error.APIError: Bad gateway
    #     # openai.error.RateLimitError
    #     return CompletionsInterface.create_completion(Coder, self.coder.id, formatted_messages, model)
    
    # def __append_message(self, content, role="user", parsed=None, error=False, task=False):
    #     message_interface = MessagesInterface(Coder, self.coder.id)
    #     new_message = message_interface.create_message({ "role": role, "content": content, "error": error, "task": task, "parsed": parsed })
    #     self.messages.append(new_message)

    # def __append_task_message(self):
    #     task = self.coder.tasks[self.coder.current_task_index]
    #     content = textwrap.dedent(f"""
    #     TASK: {task}
    #     """).strip()
        
    #     self.__append_message(content, role="user", error=False, task=True)

    # def __next_task(self):
    #     if self.coder.current_task_index == len(self.coder.tasks) - 1:
    #         self.coder.complete = True
    #         self.coder.save()
    #         return False
    #     else:
    #         self.coder.current_task_index += 1
    #         self.coder.save()
    #         self.__append_task_message()
    #         return True