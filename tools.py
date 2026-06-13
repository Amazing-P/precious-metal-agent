from analysis import calculate_vwap as vwap_function
from analysis import calculate_spread, classify_trend
from risk import assess_risk


MOCK_PRICES = [
    {"timestamp": "2026-06-11T09:00:00", "metal": "gold", "price": 2350.50, "volume": 120, "bid": 2350.00, "ask": 2351.00, "source": "london"},
    {"timestamp": "2026-06-11T09:01:00", "metal": "gold", "price": 2352.00, "volume": 150, "bid": 2351.50, "ask": 2352.50, "source": "london"},
    {"timestamp": "2026-06-11T09:02:00", "metal": "gold", "price": 2355.00, "volume": 180, "bid": 2354.50, "ask": 2355.50, "source": "nyc"},
    {"timestamp": "2026-06-11T09:03:00", "metal": "gold", "price": 2353.00, "volume": 160, "bid": 2352.50, "ask": 2353.50, "source": "nyc"},
    {"timestamp": "2026-06-11T09:04:00", "metal": "gold", "price": 2200.00, "volume": 20, "bid": 2198.00, "ask": 2202.00, "source": "nyc"},
    {"timestamp": "2026-06-11T09:00:00", "metal": "silver", "price": 30.25, "volume": 500, "bid": 30.20, "ask": 30.30, "source": "global"},
    {"timestamp": "2026-06-11T09:01:00", "metal": "silver", "price": 30.35, "volume": 550, "bid": 30.30, "ask": 30.40, "source": "global"},
]


MOCK_INVENTORY = {
    "gold": 500,
    "silver": 5000,
    "platinum": 100,
}


def get_price(metal: str = "gold") -> dict:
    """
    Get the latest price for a metal.
    """

    metal_prices = [
        item for item in MOCK_PRICES
        if item["metal"] == metal
    ]

    if not metal_prices:
        return {"error": f"No prices found for {metal}"}

    return metal_prices[-1]


def get_trend(metal: str = "gold") -> dict:
    """
    Get bullish, bearish, or neutral trend for a metal.
    """

    metal_prices = [
        item for item in MOCK_PRICES
        if item["metal"] == metal
    ]

    trend = classify_trend(metal_prices, window=2)

    return {
        "metal": metal,
        "trend": trend
    }


def calculate_vwap(metal: str = "gold") -> dict:
    """
    Calculate VWAP for a metal.
    """

    metal_prices = [
        item for item in MOCK_PRICES
        if item["metal"] == metal
    ]

    value = vwap_function(metal_prices)

    return {
        "metal": metal,
        "vwap": value
    }


def check_inventory(metal: str = "gold") -> dict:
    """
    Check available inventory for a metal.
    """

    return {
        "metal": metal,
        "inventory": MOCK_INVENTORY.get(metal, 0)
    }


def compare_spreads(metal: str = "gold") -> dict:
    """
    Compare average, max, and min spread for a metal.
    """

    metal_prices = [
        item for item in MOCK_PRICES
        if item["metal"] == metal
    ]

    spread = calculate_spread(metal_prices)

    return {
        "metal": metal,
        "spread": spread
    }


def get_recommendation(metal: str = "gold") -> dict:
    metal_prices = [
        item for item in MOCK_PRICES
        if item["metal"] == metal
    ]

    vwap = vwap_function(metal_prices)
    trend = classify_trend(metal_prices, window=2)
    spread = calculate_spread(metal_prices)
    risk = assess_risk(metal_prices, MOCK_INVENTORY)

    if trend == "bullish" and risk["risk_level"] == "low":
        recommendation = "buy"
    elif risk["risk_level"] == "high":
        recommendation = "reduce exposure"
    elif trend == "bearish":
        recommendation = "wait"
    else:
        recommendation = "hold"

    return {
        "metal": metal,
        "vwap": vwap,
        "trend": trend,
        "spread_pct": spread["spread_pct"],
        "risk_level": risk["risk_level"],
        "risk_score": risk["risk_score"],
        "recommendation": recommendation,
    }


AVAILABLE_TOOLS = {
    "get_price": {
        "function": get_price,
        "description": "Gets the latest market price for a metal.",
        "args": {"metal": "gold"}
    },
    "get_trend": {
        "function": get_trend,
        "description": "Classifies market trend as bullish, bearish, or neutral.",
        "args": {"metal": "gold"}
    },
    "calculate_vwap": {
        "function": calculate_vwap,
        "description": "Calculates volume-weighted average price.",
        "args": {"metal": "gold"}
    },
    "check_inventory": {
        "function": check_inventory,
        "description": "Checks current inventory for a metal.",
        "args": {"metal": "gold"}
    },
    "compare_spreads": {
        "function": compare_spreads,
        "description": "Calculates spread statistics for a metal.",
        "args": {"metal": "gold"}
    },
    "get_recommendation": {
        "function": get_recommendation,
        "description": "Combines analytics and risk into a trading recommendation.",
        "args": {"metal": "gold"}
    },
}
