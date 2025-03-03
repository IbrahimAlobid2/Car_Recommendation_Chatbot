
"""
VectorDBInterface
=================
This class, `VectorDBInterface`, is an abstract base class (ABC) that defines the required methods for any vector database implementation. It enforces a consistent API for managing collections, inserting and retrieving documents, and performing similarity searches using vector embeddings.

Usage:
------
- Defines a standard interface for interacting with vector databases.
- Implementations must provide concrete methods for connection, disconnection, collection management, and vector-based search operations.
- Supports inserting and retrieving vectorized documents for similarity searches.

Methods:
--------
1. **connect()**
   - Establishes a connection to the vector database.

2. **disconnect()**
   - Closes the connection to the vector database.

3. **is_collection_existed(collection_name: str) -> bool**
   - Checks if a collection exists in the database.

4. **list_all_collections() -> List**
   - Lists all collections in the vector database.

5. **get_collection_info(collection_name: str) -> dict**
   - Retrieves metadata about a specific collection.

6. **delete_collection(collection_name: str)**
   - Deletes a specified collection from the database.

7. **create_collection(collection_name: str, embedding_size: int, do_reset: bool = False)**
   - Creates a new collection with a given embedding size.
   - If `do_reset` is `True`, deletes any existing collection before creating a new one.

8. **insert_one(collection_name: str, text: str, vector: list, metadata: dict = None, record_id: str = None)**
   - Inserts a single document into the collection with a corresponding vector.

9. **insert_many(collection_name: str, texts: list, vectors: list, metadata: list = None, record_ids: list = None, batch_size: int = 50)**
   - Inserts multiple documents into the collection in batches.

10. **search_by_vector(collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]**
    - Performs a similarity search using a given vector.
    - Returns a list of `RetrievedDocument` instances ranked by relevance.

Dependencies:
-------------
- `abc.ABC` and `abc.abstractmethod` for enforcing an abstract base class.
- `pydantic.BaseModel` for defining the `RetrievedDocument` data structure.

"""



####
from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    text: str
    score: float

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50):
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]:
        pass
    