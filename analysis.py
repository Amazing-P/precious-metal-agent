import statistics


def calculate_vwap(prices: list[dict]) -> float:
    """
    Calculate volume-weighted average price.
    """

    if not prices:
        raise ValueError("Prices cannot be empty.")

    total_value = sum(item["price"] * item.get("volume", 0) for item in prices)
    total_volume = sum(item.get("volume", 0) for item in prices)

    if total_volume == 0:
        raise ValueError("Total volume cannot be zero.")

    return total_value / total_volume


def moving_average(prices: list[dict], window=5) -> list[float | None]:
    """
    Calculate simple moving average.
    """

    if not prices:
        raise ValueError("Prices cannot be empty.")

    if window <= 0:
        raise ValueError("Window must be greater than zero.")

    values = [item["price"] for item in prices]
    averages = []

    for index in range(len(values)):
        if index < window - 1:
            averages.append(None)
        else:
            group = values[index - window + 1:index + 1]
            averages.append(sum(group) / window)

    return averages


def detect_anomalies(prices: list[dict], window=3, threshold=2.0) -> list[dict]:
    """
    Detect price anomalies using rolling z-score.
    """

    if not prices:
        raise ValueError("Prices cannot be empty.")

    anomalies = []

    for index in range(window, len(prices)):
        current_price = prices[index]["price"]
        previous_prices = [
            item["price"] for item in prices[index - window:index]
        ]

        mean_price = statistics.mean(previous_prices)

        if len(previous_prices) < 2:
            continue

        standard_deviation = statistics.stdev(previous_prices)

        if standard_deviation == 0:
            continue

        z_score = (current_price - mean_price) / standard_deviation

        if abs(z_score) > threshold:
            item = prices[index].copy()
            item["z_score"] = z_score
            anomalies.append(item)

    return anomalies


def calculate_spread(prices: list[dict]) -> dict:
    """
    Calculate average, maximum, minimum spread and spread percentage.
    """

    if not prices:
        raise ValueError("Prices cannot be empty.")

    spreads = []
    mid_prices = []

    for item in prices:
        bid = item.get("bid")
        ask = item.get("ask")

        if bid is None or ask is None:
            continue

        spread = ask - bid
        mid_price = (bid + ask) / 2

        spreads.append(spread)
        mid_prices.append(mid_price)

    if not spreads:
        raise ValueError("No bid/ask data available.")

    average_spread = sum(spreads) / len(spreads)
    average_mid_price = sum(mid_prices) / len(mid_prices)

    return {
        "avg_spread": average_spread,
        "max_spread": max(spreads),
        "min_spread": min(spreads),
        "spread_pct": (average_spread / average_mid_price) * 100,
    }


def classify_trend(prices: list[dict], window=2) -> str:
    """
    Classify market trend as bullish, bearish, or neutral.
    """

    if len(prices) < 2 * window:
        raise ValueError("Not enough data to classify trend.")

    values = [item["price"] for item in prices]

    previous_group = values[-2 * window:-window]
    latest_group = values[-window:]

    previous_average = sum(previous_group) / window
    latest_average = sum(latest_group) / window

    if latest_average > previous_average:
        return "bullish"

    if latest_average < previous_average:
        return "bearish"

    return "neutral"