"""
Settings
========
This module defines the `Settings` class, which manages application-wide configurations using environment variables.

Usage:
------
- The `Settings` class loads configurations from an `.env` file using Pydantic's `BaseSettings`.
- It provides settings for various components, including LLM backends, API keys, and database configurations.
- Use `get_settings()` to retrieve an instance of `Settings` with all configurations loaded.

Attributes:
-----------
- **LLM & AI Backend Configuration**:
  - `GENERATION_BACKEND`, `VISION_BACKEND`, `EMBEDDING_BACKEND`: Specifies the backends for text generation, vision processing, and embeddings.
  - `GENERATION_MODEL_ID`, `VISION_MODEL_ID`, `EMBEDDING_MODEL_ID`: Identifiers for AI models used in different tasks.
  
- **API Keys & URLs**:
  - `OPENAI_API_KEY`, `OPENAI_API_URL`, `GROQ_API_KEY`: Credentials for OpenAI and Groq APIs.
  - `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `API_VERSION`: Azure OpenAI API configurations.
  
- **Default Processing Parameters**:
  - `INPUT_DAFAULT_MAX_CHARACTERS`, `GENERATION_DAFAULT_MAX_TOKENS`, `GENERATION_DAFAULT_TEMPERATURE`: Default settings for input processing and AI response generation.
  
- **Vector & SQL Database Configuration**:
  - `VECTOR_DB_BACKEND`, `VECTOR_DB_PATH`, `DATASET`, `DATABASE_SQL`: Paths and configurations for vector and SQL databases.
  - `COLLECTION_NAME`: Name of the vector database collection.
  
- **Classification & SQL Processing**:
  - `CLASSIFICATION_BACKEND`, `CLASSIFICATION_MODEL_ID`: Settings for classification models.
  - `SQL_BACKEND`, `SQL_MODEL_ID`: Backend and model ID for handling SQL queries.
  
Dependencies:
-------------
- `pydantic_settings` for managing settings via environment variables.

Example:
--------
```python
settings = get_settings()
print(settings.GENERATION_BACKEND)  # Outputs the configured text generation backend
```

"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    GENERATION_BACKEND: str
    VISION_BACKEND: str
    EMBEDDING_BACKEND : str 

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    GROQ_API_KEY : str = None
    
    AZURE_OPENAI_API_KEY : str = None
    AZURE_OPENAI_ENDPOINT : str = None
    API_VERSION : str = None 

    GENERATION_MODEL_ID: str = None
    VISION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID :str = None

    INPUT_DAFAULT_MAX_CHARACTERS: int = None
    GENERATION_DAFAULT_MAX_TOKENS: int = None
    GENERATION_DAFAULT_TEMPERATURE: float = None
    
    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH : str
    DATASET :str
    DATABASE_SQL:str
    COLLECTION_NAME :str
    CLASSIFICATION_BACKEND :str
    CLASSIFICATION_MODEL_ID :str
    SQL_BACKEND :str
    SQL_MODEL_ID :str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
