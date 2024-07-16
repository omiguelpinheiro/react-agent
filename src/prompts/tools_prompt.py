"""
Module Overview
---------------
This module provides a function to generate a prompt template listing available tools and their descriptions.
It helps in constructing a detailed prompt for an agent, informing it about the tools it has access to and the rules for using them.

Structure
---------
- Imports: Necessary libraries and modules.
- Function: A function to generate and return a tools prompt template.
- Example Usage: An example of how to use the function to retrieve the prompt template.

Example usage:
    from src.prompts.tools_prompt import get_tools_prompt
    from some_module import tools  # Assuming 'tools' is a list of tool objects

    prompt_template = get_tools_prompt(tools)

Note:
    The `get_tools_prompt` function should be called to retrieve the tools prompt template for use in the application.
"""

from langchain_core.tools import render_text_description

__all__ = ["get_tools_prompt"]


def get_tools_prompt(tools):
    names = [tool.name for tool in tools]
    names = ", ".join(names)
    descriptions = render_text_description(tools)
    return """
    As an agent you have access to the following tools:
    
    Names: {names}
    Documentation: {descriptions}
    
    Below is a detailed description of each tool and rules for using them.
    
    """.format(names=names, descriptions=descriptions)
