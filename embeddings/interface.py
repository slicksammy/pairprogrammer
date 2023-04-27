import uuid
import openai
import os
import re
import tiktoken
from vectordb.interface import Interface as VectorInterface
# TODO: move to environment variable - this is my personal key
openai.api_key = "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"


class Interface:
    def __init__(self):
        self.vector_collection_name = "testing"

    def embed_and_upload_code_base(self):
        excluded_files = [r"\.pyc"]
        root_path = "/Users/sam/Documents/chatgpt/news/mysite"
        vector_interface = VectorInterface(self.vector_collection_name)
        for dirpath, dirnames, filenames in os.walk(root_path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                if not any([re.search(excluded_file, file_path) for excluded_file in excluded_files]):
                    with open(file_path, "r") as f:
                        print("*"*50)
                        print(f'Processing file: {file_path}')
                        print("*"*50)
                        content = f.read()
                        chunks = self.chunk_content(content)
                        for chunk in chunks:
                            print("*"*50)
                            print(f'Processing chunk: {chunk}')
                            print("*"*50)
                            
                            summary = self.summarize_code(chunk)
                            print("*"*50)
                            print(f'Summary: {summary}')
                            print("*"*50)
                            
                            vector = self.embed(summary)
                            payload = self.generate_payload(file_path)
                            vector_interface.add_point(vector, payload)

    def embed(self, text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
    
    def chunk_content(self, content, model="gpt-3.5-turbo"):
        # encoding = tiktoken.encoding_for_model(model)
        # num_tokens = len(encoding.encode(content))
        # max_tokens = 4096
        # response_tokens = 300
        # available_prompt_tokens = max_tokens - response_tokens
        return [content]

    
    def summarize_code(self, code):
        content = f'Summarize the following code snippet:\n{code}'
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": content }]
        )

        return completion.choices[0]["message"]["content"]

    def generate_payload(self, file_path):
        return { "file_path": file_path }