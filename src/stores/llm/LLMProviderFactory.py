"""
LLMProviderFactory
==================
This class, `LLMProviderFactory`, is responsible for creating instances of different LLM providers, including OpenAI and Groq. It abstracts the initialization process by configuring the selected provider with necessary parameters.

Usage:
------
- Instantiates the factory with a configuration dictionary.
- Creates and returns an instance of the specified LLM provider.
- Supports both OpenAI and Groq providers.
- Optionally supports Azure OpenAI configurations.

Methods:
--------
1. **__init__(config: dict, azure: bool = True)**
   - Initializes the factory with a configuration dictionary and Azure support flag.

2. **create(provider: str) -> OpenAIProvider | GroqProvider | None**
   - Creates an instance of the requested LLM provider.
   - Returns `None` if the provider type is unsupported.

Dependencies:
-------------
- `LLMEnums` for provider enumeration.
- `OpenAIProvider` for OpenAI-based interactions.
- `GroqProvider` for Groq-based interactions.

"""


from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, GroqProvider
import logging

class LLMProviderFactory:
    def __init__(self, config: dict ,azure =True):
        """
        Initializes the factory with configuration values and Azure support flag.
        
        """
        self.config = config
        self.azure= azure
        
    def create(self, provider: str):
        """
        Creates an instance of the requested LLM provider based on the provided configuration.
        
        """
        if provider == LLMEnums.OPENAI.value:
            if self.azure :
                return OpenAIProvider(
                    azure_api = self.config.AZURE_OPENAI_API_KEY,
                    api_version = self.config.API_VERSION,
                    azure_endpoint = self.config.AZURE_OPENAI_ENDPOINT,
                    default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                    default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                    default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
                )
            else:
                if not self.config.OPENAI_API_KEY:
                    logging.error("Missing OpenAI API key in configuration.")
                    return None
                return OpenAIProvider(
                    api_key = self.config.OPENAI_API_KEY,
                    azure_endpoint =None ,
                    default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                    default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                    default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
                )
        elif provider == LLMEnums.GROQ.value :
            if not self.config.GROQ_API_KEY:
                logging.error("Missing Groq API key in configuration.")
                return None
            return GroqProvider(
                api_key = self.config.GROQ_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )
            
        logging.warning(f"Unsupported provider: {provider}")
        return None
