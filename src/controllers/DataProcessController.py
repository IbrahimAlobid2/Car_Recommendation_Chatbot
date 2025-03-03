"""
DataProcessController
=================
This class, `DataProcessController`, extends the `DatabaseController` and is responsible for handling the data processing operations, including file loading and data preparation for embedding.

Usage:
------
1. **File Loading:**
   - The `get_file_loader` method reads a CSV file and returns a DataFrame along with its file name.
   - Only CSV files are supported. If an unsupported file type is provided, an error is logged.

2. **Data Preparation:**
   - The `prepare_data_for_injection` method processes the DataFrame by converting each row into a structured text format.
   - It then generates embeddings for each row using the configured LLM provider.
   - Outputs include processed document strings, metadata, unique IDs, and the embeddings.

Dependencies:
-------------
- `pandas` for handling CSV files.
- `os` for file handling.
- `logging` for logging errors.
- `LLMProviderFactory` for managing LLM-related functionality.

Example:
--------
```python
process_controller = DataProcessController()
df, file_name = process_controller.get_file_loader("data/sample.csv")
docs, metadatas, ids, embeddings = process_controller.prepare_data_for_injection(df, file_name)
```

"""

from .DatabaseController import DatabaseController
import pandas as pd
import os
import logging
from stores.llm.LLMProviderFactory import LLMProviderFactory


class DataProcessController(DatabaseController):

    def __init__(self ):
        super().__init__()


       
        self.llm_provider_factory = LLMProviderFactory(self.app_settings , azure=False)
        self.client = self.llm_provider_factory.create(provider=self.app_settings.EMBEDDING_BACKEND)
        self.client.set_embedding_model(model_id = self.app_settings.EMBEDDING_MODEL_ID)
        self.logger = logging.getLogger(__name__)
        

    def get_file_loader(self, dataset: str):
        
        """
        Load a DataFrame from the specified CSV  file.
        
        Args:
            file_directory (str): The directory path of the file to be loaded.
            
        Returns:
            DataFrame, str: The loaded DataFrame and the file's base name without the extension.
            
        Raises:
            ValueError: If the file extension is neither CSV.
            
        """
        
        file_names_with_extensions = os.path.basename(dataset)
        
        file_name, file_extension = os.path.splitext(
                file_names_with_extensions)
        
        if file_extension == ".csv":
            df = pd.read_csv(dataset)
            return df, file_name
        else:
            self.logger.error("The selected file type is not supported")
            return None
        
    def prepare_data_for_injection(self, df:pd.DataFrame, file_name:str):
        docs = []
        metadatas = []
        ids = []
        embeddings = []
        
        for index, row in df.iterrows():
            output_str = ""
            # Treat each row as a separate chunk
            for col in df.columns:
                output_str += f"{col}: {row[col]},\n"
            print(f'{index} - {output_str}\n')
            embeddings.append(self.client.embed_text( output_str))
            docs.append(output_str)
            metadatas.append({"source": file_name})
            ids.append(f"id{index}")
        return docs, metadatas, ids, embeddings
    