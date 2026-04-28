import sqlite3

DB = "data/market.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        symbol TEXT,
        spot REAL,
        call_oi REAL,
        put_oi REAL,
        call_vol REAL,
        put_vol REAL,
        trend TEXT,
        direction TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_snapshot(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT INTO snapshots (time, symbol, spot, call_oi, put_oi, call_vol, put_vol, trend, direction)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["time"],
        data["symbol"],
        data["spot"],
        data["call_oi"],
        data["put_oi"],
        data["call_vol"],
        data["put_vol"],
        data["trend"],
        data["direction"]
    ))

    conn.commit()
    conn.close()