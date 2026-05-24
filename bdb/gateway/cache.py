from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class PerplexityCache:
    def __init__(self, db_path: str | Path | None = None):
        base_dir = Path(__file__).resolve().parent
        self.db_path = Path(db_path) if db_path else base_dir / "cache.db"
        self._init_db()

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    query_hash TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    ttl REAL NOT NULL
                )
                """
            )
            conn.commit()

    def get(self, query: str) -> dict[str, Any] | None:
        query_hash = self._hash(query)
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT result_json FROM cache WHERE query_hash = ? AND timestamp + ttl > ?",
                (query_hash, time.time()),
            ).fetchone()
        return json.loads(row[0]) if row else None

    def set(self, query: str, result: dict[str, Any], ttl: int = 86400) -> None:
        query_hash = self._hash(query)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache VALUES (?, ?, ?, ?, ?)",
                (query_hash, query, json.dumps(result), time.time(), ttl),
            )
            conn.commit()

    def _hash(self, query: str) -> str:
        return hashlib.sha256(query.encode("utf-8")).hexdigest()
