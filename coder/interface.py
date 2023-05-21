from coder.exceptions import InvalidAssistantResponseException, NotEnoughTokensException
from commands.interface import Interface as CommandInterface
from completions.interface import Interface as CompletionsInterface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder
import textwrap
from planner.interface import Interface as PlannerInterface
from coder.prompts.interface import Interface as PromptInterface
from .prompts.interface import Interface as PromptInterface

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
    def create_coder(cls, tasks, requirements, context, prompt_version="1"):
        coder = Coder.objects.create(
            tasks=tasks,
            requirements=requirements,
            context=context,
            current_task_index=0,
            complete=False,
        )

        prompt = PromptInterface(prompt_version, coder).prompt(context=context, tasks=tasks, requirements=requirements)
        MessagesInterface(Coder, coder.id).create_message(
            {
                "role": "user",
                "content": prompt,
                "error": False,
                "task": False
            }
        )

        # create the first task message
        instance = Interface(coder.id)
        instance.__append_task_message()

        return coder

    @classmethod
    def list(cls):
        return list(map(lambda coder: { "id" : coder.id, "tasks": coder.tasks, "requirements": coder.requirements }, list(Coder.objects.order_by("created_at").all())))

    def __init__(self, coder_id):
        self.coder = Coder.objects.get(id=coder_id)
        self.messages = MessagesInterface(Coder, coder_id).list()
        self.version = "1"

    def append_output(self, output):
        if self.messages[-1].message_content["role"] == "assistant" and self.messages[-1].message_content["error"] == False:
            content = f"""
            Output:
            {output}
            """
            self.__append_message(content, role="user")

            # the second to last message is previously the last message, the system message
            # TODO this should happen on the run step in case user has feedback
            complete = self.messages[-2].message_content["parsed"]["complete"]
            if complete:
                self.__next_task()

    def append_user_message(self, content):
        self.__append_message(content, role="user")
    
    def run(self):
        if self.coder.running:
            return
        elif self.coder.reached_max_length:
            return
        elif self.messages[-1].message_content["role"] != "assistant":
            try:
                self.__log("running", "started")
                self.coder.running = True
                self.coder.save()
                completion_interface = self.__run_completion()
                if completion_interface.reached_max_length():
                    self.coder.reached_max_length = True
                else:
                    content = completion_interface.content()
                    self.__log("response", content)
                    try:
                        # parse as save the command as a dictionary
                        parsed = PromptInterface(self.version, self.coder).parse_response(content)
                        self.__append_message(content, role="assistant", parsed=parsed)
                        self.__log("parsed", parsed)
                    except Exception as e:
                        # if you cannot parse it save the content and tell openAI there was an erro
                        self.__append_message(content, role="assistant")
                        self.__mark_previous_message_as_error()
                        self.__append_response_exception(e)
                        return
                    
                    if parsed.get("command"): # sometimes it might just be a comment
                        command_exists = CommandInterface.command_exists(parsed["command"])
                        if not command_exists:
                            self.__mark_previous_message_as_error()
                            self.__append_invalid_command(parsed["command"])
                        argument_validations = CommandInterface.validate_arguments(parsed["command"], parsed["arguments"])
                        if len(argument_validations) > 0:
                            self.__mark_previous_message_as_error()
                            self.__append_argument_validations(argument_validations)
            finally:
                self.coder.running = False
                self.coder.save()

    def status(self):
        if self.coder.running:
            return {
                "running": True
            }
        else:
            return {
                "running": False,
                "error": self.messages[-1].message_content["error"],
                "system_message": self.__current_assistant_message(),
                "reached_max_length": self.coder.reached_max_length
            }

    def __current_assistant_message(self):
        if (self.messages[-1].message_content["role"] == "assistant") and not(self.messages[-1].message_content["error"]):
            return self.messages[-1].message_content["parsed"]

    def current_task(self):
        return self.coder.tasks[self.coder.current_task_index]
    
    def complete(self):
        return self.coder.complete

    def skip_task(self):
        self.__next_task()

    def append_exception(self, e_type, e_message):
        content = f"{e_type} {e_message[:100]}"
        self.__append_message(content, role="user", error=True)

    def __log(self, name, content):
        print("*"*50)
        print(f"{name}")
        print(content)
        print("*"*50)

    def __append_response_exception(self, e):
        content = textwrap.dedent(f"""
        Could not parse your response due to:
        {e.args[0]}
        Please try again following the response format
        """).strip()
        
        self.__append_message(content, role="user", error=True)

    def __append_invalid_command(self, command):
        content = textwrap.dedent(f"""
        {command} is not a valid command
        """).strip()
        
        self.__append_message(content, role="user", error=True)

    def __append_argument_validations(self, validation_errors):
        content = textwrap.dedent(f"""
        The arguments you provided had validation errors:
        {validation_errors}
        Please try again with the proper arguments
        """).strip()
        
        self.__append_message(content, role="user", error=True)

    def __mark_previous_message_as_error(self):
        message = self.messages[-1]
        message.message_content["error"] = True
        message.save()

    # TODO configure model on coder instance
    def __run_completion(self, model="gpt-4"):
        formatted_messages = [{ "content": message.message_content["content"], "role": message.message_content["role"] } for message in self.messages]
        if CompletionsInterface.available_completion_tokens(formatted_messages, model) > 200:
            # TODO rescue openai.error.APIError: Bad gateway
            completion = CompletionsInterface.create_completion(Coder, self.coder.id, formatted_messages, model)
            return completion
        else:
            raise NotEnoughTokensException("not enough tokens available")
    
    def __append_message(self, content, role="user", parsed=None, error=False, task=False):
        message_interface = MessagesInterface(Coder, self.coder.id)
        new_message = message_interface.create_message({ "role": role, "content": content, "error": error, "task": task, "parsed": parsed })
        self.messages.append(new_message)

    def __append_task_message(self):
        task = self.coder.tasks[self.coder.current_task_index]
        content = textwrap.dedent(f"""
        TASK: {task}
        """).strip()
        
        self.__append_message(content, role="user", error=False, task=True)

    def __next_task(self):
        if self.coder.current_task_index == len(self.coder.tasks) - 1:
            self.coder.complete = True
            self.coder.save()
            return False
        else:
            self.coder.current_task_index += 1
            self.coder.save()
            self.__append_task_message()
            return True