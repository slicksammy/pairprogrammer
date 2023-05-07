import openai
openai.api_key = "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"
import tiktoken

class Interface:
    MAX_TOKENS = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8000
    }

    def available_completion_tokens(self, messages, model="gpt-3.5-turbo"):
        content = "".join(
            map(lambda x: x["content"], messages)
        )
        encoding = tiktoken.get_encoding("cl100k_base")
        max_tokens = Interface.MAX_TOKENS[model]
        return max_tokens - len(encoding.encode(content))

    # resuce openai.error.RateLimitError
    def run_completion(self, messages, model="gpt-3.5-turbo"):
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return completion["choices"][0]["message"]["content"]