import json
import re

from prompts import (
    build_tool_selection_prompt,
    build_reasoning_prompt,
    parse_llm_response,
)


class MockLLMClient:
    def generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "tool results so far" in prompt_lower:
            return json.dumps({
                "action": "answer",
                "content": self._answer_from_tool_results(prompt),
            })

        if "should i buy" in prompt_lower or "recommend" in prompt_lower:
            return """
            {
                "action": "tool",
                "tool": "get_recommendation",
                "args": {"metal": "gold"}
            }
            """

        if "vwap" in prompt_lower:
            return """
            {
                "action": "tool",
                "tool": "calculate_vwap",
                "args": {"metal": "gold"}
            }
            """

        if "trend" in prompt_lower:
            return """
            {
                "action": "tool",
                "tool": "get_trend",
                "args": {"metal": "gold"}
            }
            """

        if "inventory" in prompt_lower:
            return """
            {
                "action": "tool",
                "tool": "check_inventory",
                "args": {"metal": "gold"}
            }
            """

        if "spread" in prompt_lower:
            return """
            {
                "action": "tool",
                "tool": "compare_spreads",
                "args": {"metal": "gold"}
            }
            """

        return """
        {
            "action": "tool",
            "tool": "get_price",
            "args": {"metal": "gold"}
        }
        """

    def _answer_from_tool_results(self, prompt: str) -> str:
        tool_results = self._extract_tool_results(prompt)

        if not tool_results:
            return "I could not read the tool result."

        latest_result = tool_results[-1].get("result", {})
        tool_name = tool_results[-1].get("tool")
        metal = latest_result.get("metal", "the metal")

        if tool_name == "calculate_vwap" and "vwap" in latest_result:
            return f"The VWAP for {metal} is {latest_result['vwap']:.2f}."

        if tool_name == "get_recommendation":
            return (
                f"Recommendation for {metal}: "
                f"{latest_result['recommendation'].upper()}. "
                f"Trend is {latest_result['trend']}, "
                f"risk is {latest_result['risk_level']} "
                f"({latest_result['risk_score']}/100), "
                f"and VWAP is {latest_result['vwap']:.2f}."
            )

        return f"Tool result: {latest_result}"

    def _extract_tool_results(self, prompt: str) -> list[dict]:
        match = re.search(
            r"Tool results so far:\s*(\[.*?\])\s*Decide what to do next\.",
            prompt,
            re.DOTALL,
        )

        if not match:
            return []

        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return []


class Agent:
    def __init__(self, tools: dict, llm_client: MockLLMClient, max_iterations=5):
        self.tools = tools
        self.llm_client = llm_client
        self.max_iterations = max_iterations

    def run(self, query: str) -> dict:
        tool_results = []
        tools_called = []

        for iteration in range(1, self.max_iterations + 1):

            if not tool_results:
                prompt = build_tool_selection_prompt(query, self.tools)
            else:
                prompt = build_reasoning_prompt(query, tool_results)

            llm_output = self.llm_client.generate(prompt)
            action = parse_llm_response(llm_output)

            if action.get("action") == "answer":
                return {
                    "answer": action.get("content", ""),
                    "tools_called": tools_called,
                    "iterations": iteration,
                    "success": True,
                }

            if action.get("action") == "tool":
                tool_name = action.get("tool")
                tool_args = action.get("args", {})

                if tool_name not in self.tools:
                    tool_results.append({
                        "tool": tool_name,
                        "error": "Tool not found"
                    })
                    continue

                try:
                    tool_function = self.tools[tool_name]["function"]
                    result = tool_function(**tool_args)

                    tools_called.append(tool_name)

                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result
                    })

                except Exception as error:
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "error": str(error)
                    })

                continue

            return {
                "answer": action.get("content", "Could not parse LLM response."),
                "tools_called": tools_called,
                "iterations": iteration,
                "success": False,
            }

        return {
            "answer": "Maximum iterations reached before final answer.",
            "tools_called": tools_called,
            "iterations": self.max_iterations,
            "success": False,
        }


def run_agent_query(query: str, agent: Agent) -> dict:
    result = agent.run(query)

    if result["success"] and len(result["tools_called"]) > 0:
        confidence = 0.9
    elif result["success"]:
        confidence = 0.7
    else:
        confidence = 0.3

    result["confidence"] = confidence

    return result
