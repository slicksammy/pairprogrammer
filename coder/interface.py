from coder.response_parsers.xml import Xml
from coder.response_parsers.line import Line
from coder.response_parsers.json import Json
from coder.exceptions import InvalidAssistantResponseException, NotEnoughTokensException
from commands.interface import Interface as CommandInterface
from completions.interface import Interface as CompletionsInterface
from app_messages.interface import Interface as MessagesInterface
from .models import Coder
import textwrap
from planner.interface import Interface as PlannerInterface
from json.decoder import JSONDecodeError
import os
# TODO: move to environment variable - this is my personal key

class Interface:
    @classmethod
    def base_prompt(cls):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the v2.txt file relative to the script directory
        text_path = os.path.join(script_dir, 'prompts', 'v2.txt')

        # Open and read the v2.txt file
        with open(text_path, 'r') as file:
            return file.read()

    @classmethod
    def build_prompt(cls, context, requirements, tasks, response_prompt):
        return cls.base_prompt().replace("<<CONTEXT>>", context).replace("<<REQUIREMENTS>>", requirements).replace("<<RESPONSE_PROMPT>>", response_prompt).replace("<<TASKS>>", "\n".join(tasks))

    @classmethod
    def create_coder_from_planner(cls, planner_id):
        planner_inteface = PlannerInterface(planner_id)
        planner = planner_inteface.planner
        tasks = planner.tasks
        requirements = planner.requirements
        context = planner.context
        return cls.create_coder(tasks, requirements, context)
        

    @classmethod
    def create_coder(cls, tasks, requirements, context):
        coder = Coder.objects.create(
            tasks=tasks,
            requirements=requirements,
            context=context,
            current_task_index=0,
            complete=False,
        )

        # create the first system message
        system_message_prompt = cls.build_prompt(context, requirements, tasks, Json.response_prompt())
        MessagesInterface(Coder, coder.id).create_message(
            {
                "role": "system",
                "content": system_message_prompt,
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

    def append_output(self, output):
        if self.messages[-1].message_content["role"] == "assistant" and self.messages[-1].message_content["error"] == False:
            content = f"""
            Your previous command executed successfully.
            COMMAND OUTPUT: {output}
            Continue
            """
            self.__append_message(content, role="user")

            # the second to last message is previously the last message, the system message
            # TODO this should happen on the run step in case user has feedback
            complete = self.__parse_response(self.messages[-2].message_content["content"])["complete"]
            if complete:
                self.__next_task()

    def append_user_message(self, content):
        self.__append_message(content, role="user")
    
    def run(self):
        if self.messages[-1].message_content["role"] != "assistant":
            content = self.__run_completion()
            try:
                # parse as save the command as a dictionary
                command = self.__parse_response(content)
                self.__append_message(content, role="assistant", command=command)
            except InvalidAssistantResponseException as e:
                # if you cannot parse it save the content and tell openAI there was an erro
                self.__append_message(content, role="assistant")
                self.__mark_previous_message_as_error()
                self.__append_response_exception(e)
                return
            
            argument_validations = CommandInterface.validate_arguments(command["command"], command["arguments"])
            if len(argument_validations) > 0:
                self.__mark_previous_message_as_error()
                self.__append_argument_validations(argument_validations)

    def current_command(self):
        if (self.messages[-1].message_content["role"] == "assistant") and not(self.messages[-1].message_content["error"]):
            return self.messages[-1].message_content["command"]

    def current_task(self):
        return self.coder.tasks[self.coder.current_task_index]
    
    def complete(self):
        return self.coder.complete

    def skip_task(self):
        self.__next_task()

    def append_exception(self, e_type, e_message):
        content = f"{e_type} {e_message[:100]}"
        self.__append_message(content, role="user", error=True)

    def __append_response_exception(self, e):
        content = textwrap.dedent(f"""
        Could not parse your response due to:
        {e.args[0]}
        Please try again following the response format
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

    def __run_completion(self, model="gpt-4"):
        formatted_messages = [{ "content": message.message_content["content"], "role": message.message_content["role"] } for message in self.messages]
        completions_interface = CompletionsInterface()
        if completions_interface.available_completion_tokens(formatted_messages, model) > 200:
            return CompletionsInterface().run_completion(formatted_messages, model)
        else:
            raise NotEnoughTokensException("not enough tokens available")
    
    def __append_message(self, content, role="user", command=None, error=False, task=False):
        message_interface = MessagesInterface(Coder, self.coder.id)
        new_message = message_interface.create_message({ "role": role, "content": content, "error": error, "task": task, "command": command })
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
    
    def __response_parser_class(self):
        return Json
        
    def __parse_response(self, content):
        object = self.__response_parser_class().parse_response_object(content)
            
        if object is None:
            raise InvalidAssistantResponseException("Your response is invalid. Please follow the detailed response format")

        try:
            parsed = self.__response_parser_class().parse_object_to_dict(object)
        except JSONDecodeError:
            breakpoint()
            raise InvalidAssistantResponseException("Your provided an invalid JSON response")

        if parsed.get("command") is None:
            raise InvalidAssistantResponseException("Could not find the command")

        if parsed.get("arguments") is None:
            raise InvalidAssistantResponseException("Could not find the arguments")

        if parsed.get("summary") is None:
            raise InvalidAssistantResponseException("Could not find the summary")
        
        if parsed.get("complete") is None:
            raise InvalidAssistantResponseException("Could not find the complete")

        return parsed

    # def context(self):
    #     return """
    #     Ruby on rails probject. Ruby 3.1.2p20 (2022-04-12 revision 4491bb740a) [arm64-darwin21].
    #         """

    # def requirements(self):
    #     return """
    #     I need to build a ruby cli to communicate with my server. The cli should be used as pairprogammer COMMAND ARGUMENTS. I need this cli to be extendable.
    #     Currently the usages I have are pairprogrammer respond MESSAGE, pairprogrammer tasks, pairprogrammer messages, pairprogrammer help.
    #     """

    # def give_feedback(self, content):
    #     content = f"""
    #     I have some feedback regarding the current task:
    #     {content}

    #     Please continue responding with commands to address my feedback
    #     """

    #     self.__append_message(content)
    #    def run_command(self):
    #     last_message = self.messages[-1]
    #     if last_message["role"] == "assistant":
    #         content = last_message["content"]
    #         try:
    #             parsed_response = self.__parse_response(content)

    #             command = parsed_response["command"]
    #             arguments = parsed_response["arguments"]
    #             summary = parsed_response["summary"]
    #             explanation = parsed_response["explanation"]
    #             task = parsed_response["task"]
    #             complete = parsed_response["complete"]

    #             print("*"*50)
    #             print(f"command: {command}")
    #             print(f"arguments: {arguments}")
    #             print(f"summary: {summary}")
    #             print(f"explanation: {explanation}")
    #             print(f"task: {task}")
    #             print(f"task: {complete}")
    #             print("*"*50)

    #             response = CommandInterface().exec_command(command, arguments)
    #             if response["exception"]:
    #                 self.__mark_previous_message_as_error()
    #                 e_type = response["type"]
    #                 e_message = response["message"]
    #                 self.__append_exception(e_type, e_message)
    #                 print("*"*50)
    #                 print("command failed")
    #                 print(e_type)
    #                 print(e_message)
    #                 print("*"*50)
    #                 self.summaries.append(summary)
    #                 self.successful_commands.append({ "command": command, "arguments": arguments })
    #             else:
    #                 output = response["output"]
    #                 self.__append_output(output)
    #                 print("*"*50)
    #                 print("command succeeded")
    #                 print(output)
    #                 print("*"*50)

    #             if complete:
    #                 self.__next_task()
    #         except InvalidAssistantResponseException as e:
    #             print("*"*50)
    #             print("exception")
    #             print(e.args[0])
    #             print("*"*50)
    #             stack_trace = traceback.format_exc()
    #             print(stack_trace)
    #             self.__mark_previous_message_as_error()
    #             self.__append_response_exception(type(e), e.args[0])
    #         except Exception as e:
    #             print("*"*50)
    #             print("exception")
    #             print(e.args[0])
    #             print("*"*50)
    #             stack_trace = traceback.format_exc()
    #             print(stack_trace)
    #             self.__mark_previous_message_as_error()
    #             self.__append_exception(type(e), e.args[0])