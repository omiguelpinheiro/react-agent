"""
Module Overview
---------------
This module is designed to create and configure a ReAct (Reasoning and Acting) agent using LangChain and OpenAI's GPT-3.5-turbo model.
The agent is integrated with a set of tools, such as an SQL tool, and utilizes a memory buffer to maintain conversation history across sessions.

Structure
---------
- Imports: Necessary libraries and modules.
- Global Store: A dictionary to maintain session histories.
- Functions: Functions to handle session history retrieval.
- LLM Initialization: Setting up the language model with tools.
- Prompt Construction: Building the prompt template.
- Agent and Memory Setup: Creating the agent and memory components.

Example Usage:
    from src.agent import agent

    # Running the agent with user input
    response = agent.run({"session_id": "session_id_123", "input": "What is the target allocation percentage of stocks for each client?"})
"""

from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langgraph.checkpoint import MemorySaver
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI

import src.prompts as p
from src.logger.logger import l
from src.tools.sql import sql_tool

store = {}


l.info("Building LLM")
llm = ChatOpenAI(
    name="gpt-4o",
    temperature=0.2,
    model_kwargs={
        "seed": 42,
    },
)

l.info("Binding tools to the LLM")
tools = [StructuredTool.from_function(func=sql_tool)]
llm.bind_tools(tools)


l.info("Building prompts")
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=p.get_tools_prompt(tools)),
        SystemMessagePromptTemplate(prompt=p.get_few_shot_queries_prompt()),
        SystemMessagePromptTemplate(prompt=p.get_columns_values_prompt()),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ]
)

l.info("Initializing agent memory")
memory = MemorySaver()

l.info("Creating ReAct agent")
react_agent = create_openai_tools_agent(llm=llm, prompt=prompt, tools=tools)
agent = AgentExecutor(
    agent=react_agent,
    tools=tools,
    max_iterations=3,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
    checkpointer=memory,
)
l.info("Agent ready and waiting for input")
