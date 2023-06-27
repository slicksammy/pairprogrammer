from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
from completions.interface import Interface as CompletionInterface
import pinecone
import hashlib

pinecone.init(api_key="a7854fb2-c72a-4de6-bf99-2c80c77e564c", environment="us-west1-gcp")

class Interface:

    @classmethod
    def embed(cls, content, user):
        completion = CompletionInterface.create_completion(
            user=user,
            use_case="embedding",
            model="text-embedding-ada-002",
            messages=content
        )
        return CompletionInterface(completion=completion).message
        
    def __init__(self, user):
        self.user = user

        md5_hash = hashlib.md5()
        # TODO separate prod from dev in case of overlap
        md5_hash.update(f'{self.user.username}{self.user.date_joined}'.encode('utf-8'))
        
        self.namespace = md5_hash.hexdigest()

    def add_point(self, vector, payload):
        index = pinecone.Index("pear")
        
        index.upsert(
            vectors=[
                (
                    str(uuid.uuid4()),
                    vector,
                    payload,
                )
            ],
            namespace=self.namespace
        )

        return True
    
    def search(self, vector, limit=3):
        index = pinecone.Index("pear")

        return index.query(
            namespace=self.namespace,
            top_k=limit,
            include_values=False,
            include_metadata=True,
            vector=vector,
        )
