"""
Module Overview
---------------
This module provides a function to generate a prompt template for the possible values of columns in specific database tables.
It is designed to be used with the LangChain framework to help create syntactically correct and contextually appropriate SQL queries.

Structure
---------
- Imports: Necessary libraries and modules.
- Function: A function to generate and return a prompt template for column values.

Example usage:
    from src.prompts.columns_values_prompt import get_columns_values_prompt

    prompt_template = get_columns_values_prompt()

Note:
    The `get_columns_values_prompt` function should be called to retrieve the prompt template for use in the application.
"""

from langchain_core.prompts import PromptTemplate

__all__ = ["get_columns_values_prompt"]


def get_columns_values_prompt():
    system_columns_values_prompt = """
    Here's a list of the possible values for columns in table "allocations", correct the user message if the values are not present in the database to what you assume it to be:
    - The possible values for the column "Target Portfolio" are: Balanced, Growth, Aggressive Growth, Conservative, and Null.
    - The possible values for the column "Asset Class" are: Stocks, Bonds, ETFs, Cash, and Null.
    - The possible values for the column "Client" are: Either Client_[client_number] i.e. Client_1, or Null.
    - The possible values for the column "Target Allocation (%)" are: Any positive real number between 0 and 100.

    Here's a list of the possible values for columns in table "advisors_clients", correct the user message if the values are not present in the database to what you assume it to be:
    - The possible values for the column "Client" are: Either Client_[client_number] i.e. Client_1, or Null.
    - The possible values for the column "Sector" are: ETF, Communication Services, Technology, Consumer Discretionary, Consumer Staples, Health Care, Financials, or Null.
    - The possible values for the column "Analyst Rating" are: Hold, Buy, Sell, or Null.
    - The possible values for the column "Risk Level" are: High, Medium, Low, or Null.
    - The possible value for the columns that contain a number are: Any positive real number.
    
    Question: {input}

    Thought:{agent_scratchpad}
    """
    return PromptTemplate.from_template(system_columns_values_prompt)
