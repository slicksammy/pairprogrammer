from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import json

class CollectionAlreadyExistsException(BaseException):
        pass

class VectorCollection:
    def __init__(self, collection_name):
        self.collection_name = collection_name

class Interface:
    @classmethod
    def collection_exists(cls, collection_name):
        client = QdrantClient(host='localhost', port=6333)
        collections = client.get_collections().collections
        return any(c.name == collection_name for c in collections)

    @classmethod
    def create_collection(cls, collection_name):
        if cls.collection_exists(collection_name):
            raise CollectionAlreadyExistsException("Collection already exists")
        else:
            client = QdrantClient(host='localhost', port=6333)
            return client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )           
        
    def __init__(self, collection_name):
        self.collection = VectorCollection(collection_name)
        self.client = QdrantClient(host='localhost', port=6333)

    def add_point(self, vector, payload):
        self.client.upsert(
            collection_name=self.collection.collection_name,
            points = [
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload
                )
            ]
        )
    
    def search(self, vector, limit=3):
        return self.client.search(
            collection_name=self.collection.collection_name,
            query_vector=vector,
            limit=limit,
            with_payload=True,
        )
        
