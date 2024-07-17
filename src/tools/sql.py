"""
Module Overview
---------------
This module is designed to create and configure a SQLite database for an SQL agent using LangChain.
It includes functionality for reading CSV files into the database, checking the health of database tables,
and executing SQL queries.

Structure
---------
- Imports: Necessary libraries and modules.
- Global Variables: Paths and settings for database and CSV files.
- Functions: Functions for database connections, executing queries, and table health checks.
- Initialization: Steps to create and populate the database, and initialize the SQL agent.

Example Usage:
    from src.database import get_connection, get_cursor, execute, ping_table, sql_tool

    # Establishing a connection
    connection = get_connection()

    # Getting a cursor
    connection, cursor = get_cursor()

    # Executing a query
    connection, cursor = execute("SELECT * FROM allocations")

    # Pinging a table to check its health
    ping_table("allocations")

    # Running a custom SQL query using the sql_tool function
    result = sql_tool("SELECT * FROM allocations WHERE 'Target Portfolio' = 'Balanced'")
"""

import ast
import os
import re
import sqlite3

import pandas as pd
from langchain_community.utilities import SQLDatabase

from src.logger.logger import l


def get_connection():
    return sqlite3.connect(db_path)


def get_cursor():
    connection = get_connection()
    return connection, connection.cursor()


def execute(query: str):
    connection, cursor = get_cursor()
    cursor.execute(query)
    connection.commit()
    return connection, cursor


def ping_table(table_name: str):
    connection, cursor = execute(f"SELECT * FROM {table_name} LIMIT 1")
    try:
        rows = cursor.fetchmany(1)
        if rows and len(rows) == 1:
            l.info(f"Table {table_name} is healthy")
        else:
            l.error(f"Table {table_name} is not healthy")
            raise Exception(
                f"Table {table_name} is not healthy, something went wrong during DB creation"
            )
    except Exception as e:
        l.error(f"Error pinging table {table_name}: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


l.info("Initializing SQLAgent")
path = "/Users/miguelpinheiro/projects/interview"
db_name = "database"
csv_folder = "data"
db_path = f"{path}/{db_name}.db"
chat_history = {}

l.info(f"Creating database {db_name} in {path}")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

l.info(f"Connecting to database {db_name}")
connection = sqlite3.connect(db_path)

l.info("Reading CSV files")
allocations = pd.read_csv(f"{csv_folder}/client_target_allocations.csv")
advisors_clients = pd.read_csv(f"{csv_folder}/financial_advisor_clients.csv")

l.info("Writing CSV files to database")
allocations.to_sql("allocations", connection, if_exists="replace", index=False)
advisors_clients.to_sql(
    "advisors_clients", connection, if_exists="replace", index=False
)

connection.close()

l.info("Running health check on created tables")
ping_table("allocations")
ping_table("advisors_clients")

l.info("Initializing SQL Database tool")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

tables_columns = {
    "allocations": list(allocations.columns),
    "advisors_clients": list[advisors_clients.columns],
}


def extract_columns(query: str) -> list[str]:
    """
    Extracts the column names from a SQL SELECT query.

    Args:
        query (str): The SQL SELECT query.

    Returns:
        list[str]: A list of column names extracted from the query.
    """
    pattern = re.compile(
        r"SELECT\s+(?:DISTINCT\s+)?(.*?)\s+FROM", re.IGNORECASE | re.DOTALL
    )
    match = pattern.search(query)
    if not match:
        return []

    columns_string = match.group(1)

    column_pattern = re.compile(r"`([^`]+)`|(\b\w+\b(?:,\s*\w+\b)*)")
    matches = column_pattern.findall(columns_string)
    columns = []
    for match in matches:
        if match[0]:
            columns.append(match[0])
        elif match[1]:
            columns.extend(match[1])

    return columns


def replace_null_values(columns: list, result: str) -> str:
    """
    Replaces null values in the result list with default values based on the column name.

    Args:
        columns (list): A list of column names.
        result (str): A string representation of a list containing the query result.

    Returns:
        str: A string representation of the updated result list with null values replaced.

    Example:
        columns = ["Target Portfolio", "Asset Class", "Client"]
        result = '[[None, "Stocks", "John Doe"], ["Aggressive", None, "Unknown Client"]]'
        replace_null_values(columns, result)
        # Output: '[[Conservative, Stocks, John Doe], [Aggressive, Cash, Unknown Client]]'
    """
    default_values = {
        "Target Portfolio": "Conservative",
        "Asset Class": "Cash",
        "Client": "Unknown Client",
        "Target Allocation (%)": 0,
        "Sector": "Unknown Sector",
        "Analyst Rating": "Hold",
        "Risk Level": "Medium",
    }

    result_list = ast.literal_eval(result)

    updated_result_list = []
    for row in result_list:
        updated_row = []
        for i, value in enumerate(row):
            column_name = columns[i]
            if value is None:
                default_value = default_values.get(column_name, "Unknown")
                updated_row.append(default_value)
            else:
                updated_row.append(value)
        updated_result_list.append(updated_row)

    return str(updated_result_list)


def update_select_columns(query: str, table: str) -> str:
    """
    Updates the SELECT statement in the given SQL query to include all columns from the specified table.

    Args:
        query (str): The SQL query to update.
        table (str): The name of the table.

    Returns:
        str: The updated SQL query with the SELECT statement modified to include all columns from the table.
    """
    if f"SELECT * FROM `{table}`" in query or f"SELECT * FROM {table}" in query:
        backticked_columns = ", ".join(f"`{col}`" for col in tables_columns[table])

        query = query.replace(
            f"SELECT * FROM `{table}`",
            f"SELECT {str(backticked_columns)} FROM `{table}`",
        )

        query = query.replace(
            f"SELECT * FROM {table}",
            f"SELECT {str(backticked_columns)} FROM {table}",
        )
    return query


def replace_wildcard(query: str) -> str:
    """
    Replaces the wildcard in the given SQL query with the appropriate select columns.

    Args:
        query (str): The SQL query to be modified.

    Returns:
        str: The modified SQL query with the wildcard replaced.

    """
    if "allocations" in query:
        query = update_select_columns(query, "allocations")
    elif "advisors_clients" in query:
        query = update_select_columns(query, "advisors_clients")
    return query


def sql_tool(query: str):
    """
    Executes an SQL query using the provided query string.

    Args:
        query (str): The SQL query to be executed.

    Returns:
        The result of the SQL query execution.
    """
    query = replace_wildcard(query)
    l.info(f"Running SQL Tool with query: {query}")
    result = db.run(query)

    if not result:
        return "No results found in the database. Please try another query."

    ordered_columns = extract_columns(query)
    result = replace_null_values(ordered_columns, result)

    return result
