"""
DatabaseController
==============
This class, `DatabaseController`, provides core functionality for managing database paths and configurations.

Usage:
------
- `DatabaseController` initializes essential paths and settings from the application configuration.
- It offers methods to retrieve paths for various database-related assets.

Methods:
--------
1. **get_database_path(db_name: str) -> str**
   - Returns the path for the specified database.
   - Creates the directory if it does not exist.

2. **get_dataset_path(db_name: str) -> str**
   - Returns the path for a dataset CSV file within the database directory.

3. **get_database_sql_path(db_name: str) -> str**
   - Returns the SQL database path within the database directory.

Dependencies:
-------------
- `os` for file path operations.
- `get_settings` from `helpers.config` to retrieve application settings.

Example:
--------
```python
base_controller = DatabaseController()
db_path = base_controller.get_database_path("my_database")
print(db_path)  # Outputs the path to the database directory
```
"""
from helpers.config import get_settings
import os
import re

class DatabaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )
        
    def get_database_path(self, db_name: str):
        """
        Retrieve the database path, creating it if necessary.
        
        Args:
            db_name (str): Name of the database.
        
        Returns:
            str: Path to the database directory.
        """
        database_path = os.path.join(self.database_dir, db_name)
        if not os.path.exists(database_path):
            os.makedirs(database_path)
        return database_path
    
    def get_dataset_path(self, db_name: str):
        """
        Retrieve the dataset path for a given database.
        
        Args:
            db_name (str): Name of the database.
        
        Returns:
            str: Path to the dataset CSV file.
        """
        dataset_path = os.path.join(self.database_dir, "csv", db_name)
        return dataset_path
    
    def get_database_sql_path(self, db_name: str):
        """
        Retrieve the SQL database path for a given database.
        
        Args:
            db_name (str): Name of the database.
        
        Returns:
            str: Path to the SQL database file.
        """
        database_sql_path = os.path.join(self.database_dir, "db_sql", db_name)
        return database_sql_path
