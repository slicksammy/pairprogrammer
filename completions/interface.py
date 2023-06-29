import openai
from completions.models import Completion
import tiktoken
from django.contrib.contenttypes.models import ContentType
from openai.error import OpenAIError
from coder.models import Coder
import traceback

openai.api_key = "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"

class UnknownModelException(Exception):
    pass

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
    def log(cls, name, content=None):
        print("*"*50)
        print(name)
        print(content)
        print("*"*50)

    @classmethod
    def create_completion(cls, user, use_case, messages, model, functions=[], function_call="auto"):
        cls.log(name=f"Completions Interface - creating and running completion", content=str({
            "user": user,
            "model": model,
            "use_case": use_case,
        }))

        try:
            response = None
            message = None
            if model == "gpt-4-0613" or model == "gpt-3.5-turbo-0613":
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions,
                    function_call=function_call
                )
                message = response["choices"][0]["message"]
            elif model == "gpt-4":
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages
                )
                message = response["choices"][0]["message"]
            elif model == "text-embedding-ada-002":
                response = openai.Embedding.create(
                    input=messages,
                    model="text-embedding-ada-002"
                )
                message = response['data'][0]['embedding']
            else:
                raise UnknownModelException(f'{model} is unknown')
            
            finish_reason = None
            if "choices" in response:
                finish_reason = response["choices"][0].get("finish_reason")

            return Completion.objects.create(response=response, message=message, context_length_exceeded=(finish_reason == "length"), user=user, use_case=use_case)
        except OpenAIError as e:
            cls.log(f"Completions Interface Error - OpenAI API returned an API Error: {e}")
            return Completion.objects.create(response=None, context_length_exceeded=(e.code == 'context_length_exceeded'), message=None,  user=user, use_case=use_case, error_code=e.code, error=True)
        except UnknownModelException as e:
            cls.log("Completions Interface Error - unknown model", model)
            raise e
        except Exception as e:
            cls.log("Completions Interface Error - unknown", str(e))
            cls.log("Backtrace", traceback.format_exc())
            return Completion.objects.create(response=None, context_length_exceeded=False, message=None,  user=user, use_case=use_case, error_code="unknown", error=True)

    def __init__(self, completion=None, completion_id=None):
        self.completion = completion or Completion.objects.get(id=completion_id)
        self.message = completion.message
        self.error_code = completion.error_code
        self.error = completion.error
        self.context_length_exceeded = self.completion.context_length_exceeded