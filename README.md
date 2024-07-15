# ReAct Agent with LangChain and OpenAI

## Project Overview

This project is designed to create and configure a ReAct (Reasoning and Acting) agent using LangChain and OpenAI's GPT-4o model. The agent is integrated with a set of tools, such as an SQL tool, and utilizes a memory buffer to maintain conversation history across sessions. The goal is to enable the agent to process user queries, interact with an SQL database, and return coherent, context-aware responses.

## Table of Contents

- [ReAct Agent with LangChain and OpenAI](#react-agent-with-langchain-and-openai)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Structure](#structure)
  - [Modules](#modules)
    - [Agent Module](#agent-module)
    - [Database Module](#database-module)
    - [Logger Module](#logger-module)
    - [Prompts Module](#prompts-module)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusernamereact-agent-langchain.git cd react-agent-langchain
```

Create and activate a virtual environment:

```bash
python -m venv venv source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can use the ReAct agent directly by using:

```python
from src.agent import agent

response = agent.run({"input": "Which assets Client_1 have a target allocation smaller than 40%?"})
print(response)
```

You can interact with the agent via an API using FastAPI. Ensure you have FastAPI installed, then run the API server:

```sh
fastapi dev main.py
```

And then make requests to it:

```sh
curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "Which assets Client_1 have a target allocation smaller than 40%?"}'
```

## Structure

Below is the folder structure for this project:

```bash
.
├── README.md
├── .env
├── main.py
├── requirements.txt
├── data
│   ├── client_target_allocations.csv
│   └── financial_advisor_clients.csv
├── src
│   ├── __init__.py
│   ├── agent.py
│   ├── database.py
│   ├── logger
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── prompts
│   │   ├── __init__.py
│   │   ├── columns_values_prompt.py
│   │   ├── few_shot_queries_prompt.py
│   │   └── tools_prompt.py
│   └── tools
│       ├── __init__.py
│       └── sql.py
```

## Modules

### Agent Module

- **Description**: Sets up and configures the ReAct agent.
- **File**: src/agent.py

### Database Module

- **Description**: Creates and configures the SQLite database, reads CSV files, checks the health of tables, and executes SQL queries.
- **File**: src/database.py - **Key Functions**: <br>
  - `get_connection()`: Returns a connection to the database.<br>
  - `get_cursor()`: Returns a cursor object for executing SQL queries.<br>
  - `execute(query)`: Executes an SQL query.<br>
  - `ping_table(table_name)`: Checks if a table exists and is healthy.<br>
  - `sql_tool(query)`: The function definition for a method that queries a database and returns the result. Later transformed into a langchain tool.

### Logger Module

- **Description**: Configures the logging for the application.
- **File**: src/logger/logger.py
- **Key Functions**: - Sets up logging configuration using `logging.config.dictConfig`.

### Prompts Module

- **Description**: Provides various prompts used by the agent.
- **File**: src/prompts/
- **Key Functions**:
  - `get_tools_prompt(tools)`: Returns the prompt template for tools.<br>
  - `get_few_shot_queries_prompt()`: Returns the few-shot examples prompt template. <br>
  - `get_columns_values_prompt()`: Returns the prompt template for column values.<br>
