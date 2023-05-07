import functools
import re
from completions.interface import Interface as CompletionsInterface
from .models import Planner
import textwrap
from app_messages.interface import Interface as MessagesInterface

class Interface:
    @classmethod
    def base_prompt(cls):
        return textwrap.dedent("""
        You are a programming assistant and your job is to help the user think through their requirements for a feature they are building in their application.

        REQUIREMENTS:
        <<REQUIREMENTS>>
        
        Here is more information about their application:
        <<CONTEXT>>
        """).strip()
    
    @classmethod
    def create_planner(cls, requirements, context, description):
        planner = Planner.objects.create(
            requirements=requirements,
            context=context,
            description=description,
            tasks=[]
        )
        system_message_prompt = cls.build_prompt(context, requirements)
        MessagesInterface(Planner, planner.id).create_message(
            {
                "role": "system",
                "content": system_message_prompt,
            }
        )
        return planner

    @classmethod
    def build_prompt(cls, context, requirements):
        return cls.base_prompt().replace("<<CONTEXT>>", context).replace("<<REQUIREMENTS>>", requirements)
    
    @classmethod
    def list(cls):
        return list(map(lambda planner: { "id" : planner.id, "requirements": planner.requirements, "description": planner.description, "tasks": planner.tasks }, list(Planner.objects.order_by("created_at").all())))
    
    def __init__(self, planner_id):
        self.planner = Planner.objects.get(id=planner_id)
        self.messages = MessagesInterface(Planner, planner_id).list()

    def get_messages(self):
        return list(filter(lambda message: message["role"] != "system", list(map(lambda message: { "content": message.message_content["content"], "role": message.message_content["role"] }, self.messages))))
    
    def get_tasks(self):
        return self.planner.tasks
    
    def get_last_message(self):
        return self.messages[-1].message_content

    def run(self):
        if self.messages[-1].message_content["role"] != "assistant":
            content = self.__run_completion(messages=self.__messages_content())
            self.__append_message(content, "assistant")
    
    def respond(self, content):
        self.__append_message(content)

    def generate_tasks(self):
        content = textwrap.dedent("""
        Based on our conversation generate a list of tasks to complete the requirement in the following format:
        TASK: ...
        TASK: ...
        ...
        """).strip()

        # not including the last two messages because its just to generate tasks
        self.__append_message(content, "system")
        response = self.__run_completion(messages=self.__messages_content())
        self.__append_message(response, "assistant")
        
        tasks = re.findall(r"TASK: (.+)", response)
        self.planner.tasks = tasks
        self.planner.save()
        return tasks
    
    def __append_message(self, content, role="user"):
        message_interface = MessagesInterface(Planner, self.planner.id)
        new_message = message_interface.create_message({ "role": role, "content": content })
        self.messages.append(new_message)

    def __run_completion(self, messages, model="gpt-3.5-turbo"):
        formatted_messages = [{ "content": message["content"], "role": message["role"] } for message in messages]
        completions_interface = CompletionsInterface()
        if completions_interface.available_completion_tokens(formatted_messages, model) > 200:
            return completions_interface.run_completion(formatted_messages, model)
        else:
            raise Exception("not enough tokens")
    
    def __messages_content(self):
        return list(map(lambda message: message.message_content, self.messages))