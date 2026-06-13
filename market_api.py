class MarketAPI:
    def get_gold_prices_london(self) -> list[dict]:
        return [
            {
                "ts": "2026-06-11T09:00:00",
                "px": 2350.50,
                "vol": 120,
                "bid_px": 2350.00,
                "ask_px": 2351.00,
            },
            {
                "ts": "2026-06-11T09:01:00",
                "px": 2352.00,
                "vol": 150,
                "bid_px": 2351.50,
                "ask_px": 2352.50,
            },
        ]

    def get_gold_prices_nyc(self) -> list[dict]:
        return [
            {
                "time": "2026-06-11T09:02:00",
                "last": 2355.00,
                "qty": 180,
                "bid": 2354.50,
                "offer": 2355.50,
            },
            {
                "time": "2026-06-11T09:03:00",
                "last": 2353.00,
                "qty": 160,
                "bid": 2352.50,
                "offer": 2353.50,
            },
            {
                "time": "2026-06-11T09:04:00",
                "last": 2200.00,
                "qty": 20,
                "bid": 2198.00,
                "offer": 2202.00,
            },
        ]

    def get_silver_prices(self) -> list[dict]:
        return [
            {
                "timestamp": "2026-06-11T09:00:00",
                "price": 30.25,
                "volume": 500,
                "bid": 30.20,
                "ask": 30.30,
            },
            {
                "timestamp": "2026-06-11T09:01:00",
                "price": 30.35,
                "volume": 550,
                "bid": 30.30,
                "ask": 30.40,
            },
        ]
