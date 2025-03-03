"""
SQL_AgentController
===================
This class, `SQL_AgentController`, is responsible for handling SQL-based interactions using an LLM (Large Language Model). It allows generating, cleaning, and executing SQL queries based on natural language inputs.

Usage:
------
- `SQL_AgentController` initializes the SQL agent by setting up the prompt template and connecting to an SQLite database.
- It provides a method to process user messages, generate SQL queries, execute them, and return results.

Methods:
--------
1. **chat_agent_with_sql(message: str) -> str**
   - Takes a user query in natural language and converts it into an SQL query.
   - Executes the generated query and formats the result using an LLM.
   - Returns the final answer as a string.

Dependencies:
-------------
- `logging` for debugging and error logging.
- `DatabaseController` for accessing application settings and database paths.
- `LLMProviderFactory` and `PromptTemplate` for handling LLM-based query generation.
- `SQLDatabase` for database interactions.
- `langchain` components for chain execution and parsing.

Example:
--------
```python
llm = SomeLLMClient()  # Replace with an actual LLM client
sql_agent = SQL_AgentController(llm)
response = sql_agent.chat_agent_with_sql("How many users signed up last month?")
print(response)  # Outputs a processed response from the database query
```
"""

import logging
from .DatabaseController import DatabaseController
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.llm.PromptTemplate import get_prompt_template
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.tools import QuerySQLDatabaseTool

from langchain.chains import create_sql_query_chain
from langchain_community.agent_toolkits import create_sql_agent
import re
import os


class SQL_AgentController(DatabaseController):
    
    def __init__(self , llm):
        super().__init__()
        

        # Initialize the Prompt Template 
        self.prompt_template = get_prompt_template()
        
        self.llm = llm
        # Path to your database (db sql)
        self.database_sql_path = self.get_database_sql_path(db_name=self.app_settings.DATABASE_SQL)
        

        
    def chat_agent_with_sql(self, message: str) -> str:
        # Helper function to remove unwanted prefixes and markdown formatting from SQL output.
        def remove_markdown(sql_text: str) -> str:
            # Remove common unwanted prefixes and markdown delimiters.
            for prefix in ["SQLQuery:", "```sql", "```"]:
                sql_text = sql_text.replace(prefix, "")
            return sql_text.strip()

        # Create a runnable lambda to apply the cleaning function.
        self.remove_markdown_runnable = RunnableLambda(remove_markdown)
        
        # Generate the prompt for the SQL agent.
        # Ensure that your  returns a string template instructing the model to output only a valid SQL query.
        self.prompt = self.prompt_template.sql_agent_prompt()
        self.answer_prompt = PromptTemplate.from_template(self.prompt)
        
        # Setup the SQL database connection.
        self.db = SQLDatabase.from_uri(f"sqlite:///{self.database_sql_path}")
        
        # Setup the tool to execute SQL queries.
        self.execute_query = QuerySQLDataBaseTool(db=self.db)
        
        # Create a chain to generate the SQL query.
        write_query = create_sql_query_chain(self.llm, self.db)
        
        # Define the final chain: generate the query, remove extra text/markdown, execute the query, then use the LLM
        # to generate the final answer.
        self.answer = self.answer_prompt | self.llm | StrOutputParser()
        self.chain = (
            RunnablePassthrough.assign(query=write_query | self.remove_markdown_runnable)
            .assign(result=itemgetter("query") | self.execute_query)
            | self.answer
        )
        
        # Invoke the chain with the user's question.
        self.response = self.chain.invoke({"question": message})
        
        return self.response
    

        
        

        


