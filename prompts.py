import json
import re


def build_tool_selection_prompt(query: str, available_tools: dict) -> str:
    """
    Build the first prompt that helps the AI choose the right tool.
    """

    tool_text = []

    for name, tool in available_tools.items():
        tool_text.append(
            f"""
Tool: {name}
Description: {tool.get("description")}
Arguments: {tool.get("args")}
"""
        )

    return f"""
You are an AI assistant for a precious metals trading desk.

Available tools:
{chr(10).join(tool_text)}

User query:
{query}

Respond ONLY with valid JSON.

To call a tool:
{{
    "action": "tool",
    "tool": "tool_name",
    "args": {{}}
}}

To give final answer:
{{
    "action": "answer",
    "content": "your final answer"
}}
"""


def build_reasoning_prompt(query: str, tool_results: list) -> str:
    """
    Build a follow-up prompt after the AI has used one or more tools.
    """

    return f"""
You are an AI assistant for a precious metals trading desk.

Original user query:
{query}

Tool results so far:
{json.dumps(tool_results, indent=2)}

Decide what to do next.

Respond ONLY with valid JSON.

To call another tool:
{{
    "action": "tool",
    "tool": "tool_name",
    "args": {{}}
}}

To give final answer:
{{
    "action": "answer",
    "content": "your final answer"
}}
"""


def parse_llm_response(response: str) -> dict:
    """
    Convert the AI text response into a Python dictionary.
    Handles normal JSON, JSON in markdown, and JSON hidden inside text.
    """

    raw = response.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    code_block = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        raw,
        re.DOTALL
    )

    if code_block:
        try:
            return json.loads(code_block.group(1))
        except json.JSONDecodeError:
            pass

    json_inside_text = re.search(r"\{.*\}", raw, re.DOTALL)

    if json_inside_text:
        try:
            return json.loads(json_inside_text.group(0))
        except json.JSONDecodeError:
            pass

    return {
        "action": "error",
        "content": response
    }