"""
QdrantDBProvider
===============
This class, `QdrantDBProvider`, is an implementation of the `VectorDBInterface` that interacts with the Qdrant vector database.

Usage:
------
- Establishes a connection to a Qdrant database instance.
- Creates and manages collections for vector-based retrieval.
- Inserts and retrieves documents using vector similarity search.

Methods:
--------
1. **connect()**
   - Establishes a connection to the Qdrant database.

2. **disconnect()**
   - Closes the database connection by setting the client to `None`.

3. **is_collection_existed(collection_name: str) -> bool**
   - Checks if a given collection exists in Qdrant.

4. **list_all_collections() -> List**
   - Retrieves a list of all collections available in the database.

5. **get_collection_info(collection_name: str) -> dict**
   - Retrieves metadata and configuration details for a specified collection.

6. **delete_collection(collection_name: str)**
   - Deletes a collection if it exists.

7. **create_collection(collection_name: str, embedding_size: int, do_reset: bool = False) -> bool**
   - Creates a new collection with a given embedding size.
   - If `do_reset` is `True`, deletes an existing collection before creating a new one.

8. **insert_one(collection_name: str, text: str, vector: list, metadata: dict = None, record_id: str = None) -> bool**
   - Inserts a single document with an embedding vector into a specified collection.

9. **insert_many(collection_name: str, texts: list, vectors: list, metadata: list = None, record_ids: list = None, batch_size: int = 50) -> bool**
   - Inserts multiple documents in batches.

10. **search_by_vector(collection_name: str, vector: list, limit: int = 5) -> List[RetrievedDocument]**
    - Performs a similarity search using an embedding vector.
    - Returns a list of `RetrievedDocument` objects ranked by similarity score.

Dependencies:
-------------
- `qdrant_client` for communicating with the Qdrant vector database.
- `logging` for debugging and error tracking.
- `pydantic.BaseModel` for defining the `RetrievedDocument` structure.

Example:
--------
```python
qdrant_provider = QdrantDBProvider(db_path="./qdrant_db")
qdrant_provider.connect()
qdrant_provider.create_collection("my_collection", embedding_size=512)
response = qdrant_provider.search_by_vector("my_collection", vector=[0.1, 0.2, 0.3], limit=5)
print(response)
```

"""


from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
import logging
from typing import List
from pydantic import BaseModel

class RetrievedDocument(BaseModel):
    text: str
    score: float  # Represents how closely the document matches the query (higher = more similar)

class QdrantDBProvider(VectorDBInterface):
    """
    Implementation of VectorDBInterface for the Qdrant vector database.
    """

    def __init__(self, db_path: str):
        """
        :param db_path: Local file path for the Qdrant database.
                       If using Qdrant server, consider changing the connection approach.
        """
        self.client = None
        self.db_path = db_path
        self.distance_method = models.Distance.COSINE  # COSINE distance for similarity

        self.logger = logging.getLogger(__name__)

    def connect(self):
        """
        Establishes a connection to the local Qdrant instance using the provided db_path.
        Consider wrapping this in a try-except block if connection can fail.
        """
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        """
        Sets the Qdrant client to None to release resources.
        Consider checking if 'self.client' is already None before setting again.
        """
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        """
        Checks if a specific collection is present in Qdrant.

        :param collection_name: The name of the collection to check.
        :return: True if the collection exists, False otherwise.
        """
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        """
        Retrieves all available collections in Qdrant.

        :return: A list of collection metadata or collection names.
        """
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        """
        Gets detailed information for a single collection.

        :param collection_name: The name of the collection to inspect.
        :return: A dictionary of collection metadata.
        """
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        """
        Deletes an existing collection if it exists.

        :param collection_name: The name of the collection to delete.
        :return: The result of the deletion request. Could be None if no collection is found.
        """
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        
    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False) -> bool:
        """
        Creates a new collection with the given embedding size.

        :param collection_name: Name of the new collection.
        :param embedding_size: The dimensionality of the embedding vectors.
        :param do_reset: If True, deletes any existing collection with the same name before creating.
        :return: True if a new collection was created, False otherwise.
        """
        if do_reset:
            # If do_reset is True, remove the collection if it exists.
            _ = self.delete_collection(collection_name=collection_name)
        
        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True
        
        return False
    
    def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None) -> bool:
        """
        Inserts a single record into the specified collection.

        :param collection_name: Collection name to insert into.
        :param text: The raw text data.
        :param vector: The embedding vector corresponding to the text.
        :param metadata: Optional dictionary of additional metadata.
        :param record_id: Unique identifier for this record. Provide a stable ID to avoid duplicates.
        :return: True if successful, False otherwise.
        """
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"Cannot insert record to non-existent collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=[record_id],
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting record: {e}")
            return False

        return True
    
    def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50) -> bool:
        """
        Inserts multiple records into the specified collection in batches.

        :param collection_name: Name of the collection.
        :param texts: List of text data entries.
        :param vectors: List of embedding vectors, same length as texts.
        :param metadata: Optional list of metadata dictionaries, same length as texts.
        :param record_ids: Optional list of unique IDs for each record.
        :param batch_size: How many records to insert per upload call to Qdrant.
        :return: True if all inserts succeed, False otherwise.
        """
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_records = [
                models.Record(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": batch_metadata[x]
                    }
                )
                for x in range(len(batch_texts))
            ]

            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch [{i}:{batch_end}]: {e}")
                return False

        return True
        
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5) -> List[RetrievedDocument]:
        """
        Performs a similarity search in the specified collection.

        :param collection_name: The collection to search within.
        :param vector: The query embedding vector.
        :param limit: The maximum number of matching records to return.
        :return: A list of RetrievedDocument objects (text and score) or None if no matches.
        """
        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results) == 0:
            return None  # Return None or an empty list for no results
        
        return [
            RetrievedDocument(
                score=result.score,
                text=result.payload["text"]
            )
            for result in results
        ]
