from analysis import (
    calculate_spread,
    detect_anomalies,
    classify_trend,
)


def assess_risk(
    prices: list[dict],
    inventory: dict,
    config: dict | None = None
) -> dict:
    """
    Assess trading risk using market and inventory signals.

    Risk factors:
    1. Wide spreads
    2. Price anomalies
    3. Low inventory coverage
    4. Bearish trend
    5. Declining volume
    """

    if not prices:
        raise ValueError("Prices cannot be empty.")

    if config is None:
        config = {
            "wide_spread_pct": 0.5,
            "high_anomaly_count": 1,
            "low_inventory_coverage": 2.0,
            "volume_decline_pct": 25,
        }

    risk_score = 0
    factors = []

    spread_data = calculate_spread(prices)

    if spread_data["spread_pct"] > config["wide_spread_pct"]:
        risk_score += 25
        factors.append("Wide spreads suggest market stress.")

    anomaly_window = min(3, max(2, len(prices) // 2))

    anomalies = detect_anomalies(
        prices,
        window=anomaly_window,
        threshold=2.0
    )

    if len(anomalies) >= config["high_anomaly_count"]:
        risk_score += 25
        factors.append("Multiple price anomalies suggest volatility.")

    total_volume = sum(item.get("volume", 0) for item in prices)
    average_volume = total_volume / len(prices)

    latest_metal = prices[-1]["metal"]
    available_inventory = inventory.get(latest_metal, 0)

    if average_volume == 0:
        inventory_coverage = 0
    else:
        inventory_coverage = available_inventory / average_volume

    if inventory_coverage < config["low_inventory_coverage"]:
        risk_score += 20
        factors.append("Inventory is low compared with trading volume.")

    try:
        trend_window = min(2, len(prices) // 2)
        trend = classify_trend(prices, window=trend_window)
    except ValueError:
        trend = "unknown"

    if trend == "bearish":
        risk_score += 15
        factors.append("Bearish trend increases downside risk.")

    previous_volumes = [
        item.get("volume", 0) for item in prices[:-1]
    ]
    latest_volume = prices[-1].get("volume", 0)

    if previous_volumes:
        previous_average_volume = sum(previous_volumes) / len(previous_volumes)
    else:
        previous_average_volume = latest_volume

    if previous_average_volume > 0:
        volume_decline_pct = (
            (previous_average_volume - latest_volume) / previous_average_volume
        ) * 100
    else:
        volume_decline_pct = 0

    if volume_decline_pct > config["volume_decline_pct"]:
        risk_score += 15
        factors.append("Volume is declining, which may signal liquidity risk.")

    if risk_score >= 70:
        risk_level = "high"
        trading_signal = "reduce exposure"
    elif risk_score >= 40:
        risk_level = "medium"
        trading_signal = "trade carefully"
    else:
        risk_level = "low"
        trading_signal = "normal trading conditions"

    return {
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "trading_signal": trading_signal,
        "factors": factors,
        "spread": spread_data,
        "trend": trend,
        "anomaly_count": len(anomalies),
        "inventory_coverage": inventory_coverage,
        "volume_decline_pct": volume_decline_pct,
    }
