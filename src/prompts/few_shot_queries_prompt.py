"""
Module Overview
---------------
This module provides a function to generate a few-shot prompt template for generating SQL queries based on user inputs.
It uses LangChain's FewShotPromptTemplate, example selectors, and OpenAI embeddings to construct the prompt.

Structure
---------
- Imports: Necessary libraries and modules.
- Function: A function to generate and return a few-shot prompt template for SQL queries.
- Example Queries: A function to provide example input-query pairs.

Example usage:
    from src.prompts.few_shot_queries_prompt import get_few_shot_queries_prompt

    prompt_template = get_few_shot_queries_prompt()

Note:
    The `get_few_shot_queries_prompt` function should be called to retrieve the prompt template for use in the application.
"""

from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import OpenAIEmbeddings

__all__ = ["get_few_shot_queries_prompt"]


def get_examples():
    return [
        {
            "input": "What is the target allocation percentage of stocks for each client?",
            "query": 'SELECT "Client", "Target Allocation (%)" FROM allocations WHERE "Asset Class" = \'Stocks\';',
        },
        {
            "input": "List all clients with a 'Balanced' target portfolio and their respective asset classes.",
            "query": 'SELECT "Client", "Asset Class" FROM allocations WHERE "Target Portfolio" = \'Balanced\';',
        },
        {
            "input": "Which clients have an allocation in bonds greater than 20%?",
            "query": 'SELECT "Client" FROM allocations WHERE "Asset Class" = \'Bonds\' AND "Target Allocation (%)" > 20;',
        },
        {
            "input": "Show the total allocation percentage for each asset class for Client_1.",
            "query": 'SELECT "Asset Class", SUM("Target Allocation (%)") as "Total Allocation" FROM allocations WHERE "Client" = \'Client_1\' GROUP BY "Asset Class";',
        },
        {
            "input": "Find clients with 'Aggressive Growth' portfolios and their allocations in ETFs.",
            "query": 'SELECT "Client", "Target Allocation (%)" FROM allocations WHERE "Target Portfolio" = \'Aggressive Growth\' AND "Asset Class" = \'ETFs\';',
        },
        {
            "input": "What are the target allocations for all asset classes in the 'Conservative' portfolio?",
            "query": 'SELECT "Asset Class", "Target Allocation (%)" FROM allocations WHERE "Target Portfolio" = \'Conservative\';',
        },
        {
            "input": "List all clients and their total target allocation in stocks.",
            "query": 'SELECT "Client", SUM("Target Allocation (%)") as "Total Stock Allocation" FROM allocations WHERE "Asset Class" = \'Stocks\' GROUP BY "Client";',
        },
        {
            "input": "Show the target allocation for each client who has a 'Growth' portfolio.",
            "query": 'SELECT "Client", "Asset Class", "Target Allocation (%)" FROM allocations WHERE "Target Portfolio" = \'Growth\';',
        },
        {
            "input": "Which clients have more than 50% allocation in any single asset class?",
            "query": 'SELECT "Client", "Asset Class", "Target Allocation (%)" FROM allocations WHERE "Target Allocation (%)" > 50;',
        },
        {
            "input": "List the target portfolios that do not have a specified client.",
            "query": 'SELECT "Target Portfolio", "Asset Class", "Target Allocation (%)" FROM allocations WHERE "Client" IS NULL;',
        },
    ]


def get_few_shot_queries_prompt():
    system_few_shot_prefix = """
    Given an input question and considering the context of previous conversations, create a syntactically correct SQL query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. Only SELECT statements are allowed.

    Consider the following examples of user inputs and their corresponding SQL queries, as well as the context of previous conversations to provide accurate and relevant responses:

    Here are some examples of user inputs and their corresponding SQL queries:
    """.format(
        top_k=3
    )

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        get_examples(),
        OpenAIEmbeddings(model="text-embedding-ada-002"),
        FAISS,
        k=5,
        input_keys=["input"],
    )

    return FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input"],
        prefix=system_few_shot_prefix,
        suffix="",
    )
