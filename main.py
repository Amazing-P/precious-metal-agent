import sqlite3
from pprint import pprint

from market_api import MarketAPI
from pipeline import fetch_all_prices, store_prices
from analysis import (
    calculate_vwap,
    moving_average,
    detect_anomalies,
    calculate_spread,
    classify_trend,
)
from risk import assess_risk
from tools import AVAILABLE_TOOLS, MOCK_INVENTORY
from agent import Agent, MockLLMClient, run_agent_query


def prices_by_metal(prices: list[dict]) -> dict[str, list[dict]]:
    grouped = {}

    for item in prices:
        grouped.setdefault(item["metal"], []).append(item)

    return grouped


def print_analysis(metal: str, metal_prices: list[dict]) -> None:
    print(f"\n{metal.title()}:")

    try:
        vwap = calculate_vwap(metal_prices)
        print(f"VWAP: {vwap:.2f}")
    except ValueError as error:
        print(f"VWAP error: {error}")

    try:
        window = min(2, len(metal_prices))
        ma = moving_average(metal_prices, window=window)
        print("Moving average:")
        pprint(ma)
    except ValueError as error:
        print(f"Moving average error: {error}")

    try:
        anomalies = detect_anomalies(metal_prices, window=2, threshold=2.0)
        print("Anomalies:")
        pprint(anomalies)
    except ValueError as error:
        print(f"Anomaly error: {error}")

    try:
        spread = calculate_spread(metal_prices)
        print("Spread:")
        pprint(spread)
    except ValueError as error:
        print(f"Spread error: {error}")

    try:
        window = min(2, len(metal_prices) // 2)
        trend = classify_trend(metal_prices, window=window)
        print(f"Trend: {trend}")
    except ValueError as error:
        print(f"Trend error: {error}")


def print_risk(metal: str, metal_prices: list[dict]) -> None:
    print(f"\n{metal.title()}:")

    try:
        risk_result = assess_risk(metal_prices, MOCK_INVENTORY)
        pprint(risk_result)
    except ValueError as error:
        print(f"Risk assessment error: {error}")


def main():
    print("\n=== PRECIOUS METALS AI AGENT ===\n")

    api = MarketAPI()
    prices = fetch_all_prices(api)

    print("Fetched and normalised prices:")
    pprint(prices)

    if not prices:
        print("No valid prices found. Exiting.")
        return

    with sqlite3.connect(":memory:") as db:
        inserted_count = store_prices(db, prices)

    print(f"\nRows inserted into database: {inserted_count}")

    print("\n=== ANALYSIS RESULTS ===")

    grouped_prices = prices_by_metal(prices)

    for metal, metal_prices in grouped_prices.items():
        print_analysis(metal, metal_prices)

    print("\n=== RISK ASSESSMENT ===")

    for metal, metal_prices in grouped_prices.items():
        print_risk(metal, metal_prices)

    print("\n=== AGENT TEST ===")

    llm_client = MockLLMClient()

    agent = Agent(
        tools=AVAILABLE_TOOLS,
        llm_client=llm_client,
        max_iterations=5,
    )

    query = "Should I buy gold?"

    agent_result = run_agent_query(query, agent)

    print(f"User query: {query}")
    pprint(agent_result)

    print("\nProject ran successfully.")


if __name__ == "__main__":
    main()
