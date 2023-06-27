import openai
from completions.models import Completion
openai.api_key = "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"
import tiktoken
from django.contrib.contenttypes.models import ContentType
from openai.error import OpenAIError
from coder.models import Coder

class Interface:
    MAX_TOKENS = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8000,
        "gpt-4-0613": 8000
    }

    @classmethod
    def available_completion_tokens(self, messages, model="gpt-4"):
        content = "".join(
            map(lambda x: x.message_content["content"], messages)
        )
        encoding = tiktoken.get_encoding("cl100k_base")
        max_tokens = Interface.MAX_TOKENS[model]
        return max_tokens - len(encoding.encode(content))

    @classmethod
    def create_completion(cls, coder_id, messages, model, functions=None, function_call="auto"):
        print("*"*50)
        print("running completion")
        print(model)
        print("*"*50)

        try:
            response = None
            if functions is not None:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions,
                    function_call=function_call
                )
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages
                )
            
            message = response["choices"][0]["message"]
            return Completion.objects.create(response=response, message=message, context_length_exceeded=(response["choices"][0]["finish_reason"] == "length"), completer_type=ContentType.objects.get_for_model(Coder), completer_id=coder_id)
        except OpenAIError as e:
            return Completion.objects.create(response=None, context_length_exceeded=(e.code == 'context_length_exceeded'), message=None, completer_type=ContentType.objects.get_for_model(Coder), completer_id=coder_id, error_code=e.code, error=True)
        except Exception as e:
            return Completion.objects.create(response=None, context_length_exceeded=False, message=None, completer_type=ContentType.objects.get_for_model(Coder), completer_id=coder_id, error_code="unknown", error=True)

    @classmethod
    def most_recent_completion(cls, coder_id):
       return Completion.objects.filter(completer_type=ContentType.objects.get_for_model(Coder), completer_id=coder_id).order('-created_at').first()

    def __init__(self, completion=None, completion_id=None):
        self.completion = completion or Completion.objects.get(id=completion_id)
        self.message = completion.message
        self.error_code = completion.error_code
        self.error = completion.error
        self.context_length_exceeded = self.context_length_exceeded