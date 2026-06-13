import sqlite3

def fetch_all_prices(api, max_retries=3) -> list[dict]:
    endpoints = [
        ("gold", "London", api.get_gold_prices_london,
         {"timestamp": "ts", "price": "px", "volume": "vol",
          "bid": "bid_px", "ask": "ask_px"}),
        ("gold", "New York", api.get_gold_prices_nyc,
         {"timestamp": "time", "price": "last", "volume": "qty",
          "bid": "bid", "ask": "offer"}),
        ("silver", "Global", api.get_silver_prices,
         {"timestamp": "timestamp", "price": "price", "volume": "volume",
          "bid": "bid", "ask": "ask"}),
    ]

    prices = []
    seen = set()

    for metal, source, fetch_function, mapping in endpoints:
        records = None

        for _ in range(max_retries):
            try:
                records = fetch_function()
                break
            except ConnectionError:
                records = None

        if records is None:
            continue

        for record in records:
            price = record.get(mapping["price"])

            if price is None:
                continue

            clean_record = {
                "timestamp": record.get(mapping["timestamp"]),
                "metal": metal,
                "price": price,
                "volume": record.get(mapping["volume"], 0),
                "bid": record.get(mapping["bid"]),
                "ask": record.get(mapping["ask"]),
                "source": source,
            }

            key = (
                clean_record["timestamp"],
                clean_record["metal"],
                clean_record["source"],
            )

            if key in seen:
                continue

            seen.add(key)
            prices.append(clean_record)

    return prices


def store_prices(db: sqlite3.Connection, prices: list[dict]) -> int:
    """
    Store prices in SQLite and skip duplicate records.
    """

    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            metal TEXT NOT NULL,
            price REAL NOT NULL,
            volume REAL,
            bid REAL,
            ask REAL,
            source TEXT NOT NULL,
            UNIQUE(timestamp, metal, source)
        )
    """)

    inserted = 0

    for item in prices:
        try:
            cursor.execute("""
                INSERT INTO prices (
                    timestamp, metal, price, volume, bid, ask, source
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["timestamp"],
                item["metal"],
                item["price"],
                item["volume"],
                item["bid"],
                item["ask"],
                item["source"],
            ))

            inserted += 1

        except sqlite3.IntegrityError:
            continue

    db.commit()
    return inserted
