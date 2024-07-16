"""
Module Overview
---------------
This module provides a function to generate a system prompt template containing rules for using the SQL tool.
The prompt guides the user on how to interact with the SQL database, including proper syntax and constraints.

Structure
---------
- Imports: Necessary libraries and modules (if any).
- Function: A function to generate and return the SQL tool rules prompt template.
- Example Usage: An example of how to use the function to retrieve the prompt template.

Example usage:
    from src.prompts.sql_tool_rules_prompt import get_sql_tool_rules_prompt

    prompt_template = get_sql_tool_rules_prompt()

Note:
    The `get_sql_tool_rules_prompt` function should be called to retrieve the SQL tool rules prompt template for use in the application.
"""

__all__ = ["get_sql_tool_rules_prompt"]


def get_sql_tool_rules_prompt():
    return """\
    The SQL tool enables interaction with a SQL Database. You can query the database schema, the columns, and values. The tool
    will return either a string containing the rows of the query or an empty string if there's no result for the query, act accordingly.
    
    About the values in the database:
    
    The possible values for columns in table "allocations":
    - The possible values for the column "Target Portfolio" are: Balanced, Growth, Aggressive Growth, Conservative, and Null.
    - The possible values for the column "Asset Class" are: Stocks, Bonds, ETFs, Cash, and Null.
    - The possible values for the column "Client" are: Either Client_[client_number] i.e. Client_1, or Null.
    - The possible values for the column "Target Allocation (%)" are: Any positive real number between 0 and 100.

    The possible values for columns in table "advisors_clients":
    - The possible values for the column "Client" are: Either Client_[client_number] i.e. Client_1, or Null.
    - The possible values for the column "Sector" are: ETF, Communication Services, Technology, Consumer Discretionary, Consumer Staples, Health Care, Financials, or Null.
    - The possible values for the column "Analyst Rating" are: Hold, Buy, Sell, or Null.
    - The possible values for the column "Risk Level" are: High, Medium, Low, or Null.
    - The possible value for the columns that contain a number are: Any positive real number.
    
    When dealing with null values found in the database:
    - If a column has a null value, the value will be represented as Null.
    
    When using this tool, make sure to:
    - Use the correct SQL syntax. 
    - Always to put column and table names around `` since it's possible for them to have spaces or special characters.
    - Only query the tables that are available
    - Only query the columns that are available
    - Only query the values that are available
    - Before using the tool, if it's not clear what to query in the database, make any questions to make the tool usage more efficient.
    - By no means make DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. Only SELECT statements are allowed.
    - Correct the user message if the values are not present in the database to what you assume it to be i.e. If the user asks for a ETFs, that's not a value of Asset Class column, but ETF is.
    - Only query what is available in the database, if the user asks for a value that is not present in the database, return an empty string.
    """
