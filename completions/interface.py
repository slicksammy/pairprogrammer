import openai
from completions.models import Completion
openai.api_key = "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"
import tiktoken
from django.contrib.contenttypes.models import ContentType

class Interface:
    MAX_TOKENS = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8000
    }

    @classmethod
    def available_completion_tokens(self, messages, model="gpt-3.5-turbo"):
        content = "".join(
            map(lambda x: x.message_content["content"], messages)
        )
        encoding = tiktoken.get_encoding("cl100k_base")
        max_tokens = Interface.MAX_TOKENS[model]
        return max_tokens - len(encoding.encode(content))

    @classmethod
    def create_completion(cls, completer_type, completer_id, messages, model="gpt-3.5-turbo"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        content = response["choices"][0]["message"]["content"]
        completion = Completion(response=response, content=content, completer_type=ContentType.objects.get_for_model(completer_type), completer_id=completer_id)
        completion.save()
        return Interface(completion=completion)

    def __init__(self, completion=None, completion_id=None):
        self.completion = completion or Completion.objects.get(id=completion_id)

    def reached_max_length(self):
        return self.completion.response["choices"][0]["finish_reason"] == "length"

    def content(self):
        return self.completion.content