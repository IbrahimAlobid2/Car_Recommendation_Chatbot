"""
LLMInterface
============
This module defines the `LLMInterface` class, which serves as an abstract base class (ABC) for any Large Language Model (LLM) interface implementation.

Usage:
------
- `LLMInterface` defines methods that must be implemented by any subclass providing LLM-based functionality.
- It enforces the implementation of methods for setting models, generating text, processing vision inputs, and constructing prompts.

Methods:
--------
1. **set_generation_model(model_id: str) -> None**
   - Sets the model ID for text generation.

2. **set_vision_model(model_id: str) -> None**
   - Sets the model ID for vision processing.

3. **generate_text(prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None) -> str**
   - Generates text based on the given prompt and optional parameters.

4. **LLM_CHAT()**
   - Placeholder method for interactive chat functionalities.

5. **vision_to_text(uploaded_image, prompt: str)**
   - Processes an uploaded image and extracts textual details based on the provided prompt.

6. **construct_prompt(prompt: str, role: str) -> dict**
   - Constructs and returns a structured prompt for the LLM.

"""


from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str) -> None:
        pass

    @abstractmethod
    def set_vision_model(self, model_id: str) -> None:
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None) -> str:
        pass


    @abstractmethod
    def LLM_CHAT(self):
        pass
    
    
    @abstractmethod
    def vision_to_text(self, uploaded_image, prompt:str):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str)-> dict:
        pass
