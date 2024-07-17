"""
Module Overview
---------------
This module is designed to create and configure a ReAct (Reasoning and Acting) agent using LangChain and OpenAI's GPT-3.5-turbo model.
The agent is integrated with a set of tools, such as an SQL tool, and utilizes a memory buffer to maintain conversation history across sessions.

Structure
---------
- Imports: Necessary libraries and modules.
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
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI

import src.prompts as p
from src.logger.logger import l
from src.tools.sql import sql_tool

l.info("Building LLM")
llm = ChatOpenAI(
    name="gpt-4o",
    temperature=0,
    model_kwargs={
        "seed": 42,
    },
)

l.info("Binding tools to the LLM")
tools = [StructuredTool.from_function(func=sql_tool, handle_tool_error=True)]
llm.bind_tools(tools)


l.info("Building prompts")
system_prompt = PromptTemplate.from_template(
    "".join(
        [
            p.get_agent_description_prompt(),
            p.get_tools_prompt(tools),
            p.get_sql_tool_rules_prompt(),
        ]
    )
)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ]
)

l.info("Initializing agent memory")

memory = ChatMessageHistory(session_id="test-session")

l.info("Creating ReAct agent")
react_agent = create_openai_tools_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(
    agent=react_agent,
    tools=tools,
    max_iterations=3,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)

agent = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)
l.info("Agent ready and waiting for input")
