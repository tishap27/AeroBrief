import json
import sqlite3
import time
from contextlib import closing

DB = "cache.db"
TTL = 300  # seconds


def _conn():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT, ts REAL)")
    return c


def get(key):
    with closing(_conn()) as c:
        row = c.execute("SELECT value, ts FROM cache WHERE key=?", (key,)).fetchone()
    if row and time.time() - row[1] < TTL:
        return json.loads(row[0])
    return None


def put(key, value):
    with closing(_conn()) as c:
        c.execute("INSERT OR REPLACE INTO cache VALUES (?,?,?)",
                  (key, json.dumps(value), time.time()))
        c.commit()