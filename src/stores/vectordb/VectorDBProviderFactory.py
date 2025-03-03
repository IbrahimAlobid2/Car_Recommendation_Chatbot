"""
VectorDBProviderFactory
========================
This class, `VectorDBProviderFactory`, is responsible for creating instances of vector database providers.

Usage:
------
- Instantiates the factory with a configuration object.
- Uses `DatabaseController` to fetch the database path.
- Supports the creation of both `QdrantDBProvider` and `ChromaDBProvider` instances.
- Returns `None` if an unsupported provider type is specified.

Methods:
--------
1. **__init__(config)**
   - Initializes the factory with a configuration object.

2. **create(provider: str) -> QdrantDBProvider | ChromaDBProvider | None**
   - Creates an instance of the requested vector database provider.
   - Returns `None` if the provider is not supported.

Dependencies:
-------------
- `QdrantDBProvider` for Qdrant-based vector database operations.
- `ChromaDBProvider` for Chroma-based vector database operations.
- `VectorDBEnums` for provider type enumeration.
- `DatabaseController` for managing database paths.

"""
from .providers import QdrantDBProvider
from .providers import ChromaDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers.DatabaseController import DatabaseController

class VectorDBProviderFactory:
    """
    Factory class to create vector database provider instances.
    """
    
    def __init__(self, config):
        """
        Initializes the factory with the provided configuration.
        
        :param config: Configuration object containing database settings.
        """
        self.config = config
        self.base_controller = DatabaseController()

    def create(self, provider: str):
        """
        Creates and returns an instance of the specified vector database provider.
        
        :param provider: The type of vector database provider to create.
        :return: An instance of `QdrantDBProvider` or `ChromaDBProvider`, or `None` if the provider is invalid.
        """
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(db_path=db_path)
        elif provider == VectorDBEnums.CHROMA.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return ChromaDBProvider(db_path=db_path)
        return None
