from __future__ import annotations

import sqlite3
import time
from pathlib import Path


class RateLimiter:
    def __init__(self, db_path: str | Path | None = None, limit: int = 100, window_seconds: int = 86400):
        base_dir = Path(__file__).resolve().parent
        self.db_path = Path(db_path) if db_path else base_dir / "rate_limiter.db"
        self.limit = limit
        self.window_seconds = window_seconds
        self._init_db()

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS limits (
                    user_id TEXT PRIMARY KEY,
                    count INTEGER NOT NULL,
                    window_start REAL NOT NULL
                )
                """
            )
            conn.commit()

    def check_limit(self, user_id: str) -> bool:
        current_time = time.time()
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT count, window_start FROM limits WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            if not row:
                conn.execute(
                    "INSERT INTO limits VALUES (?, ?, ?)",
                    (user_id, 1, current_time),
                )
                conn.commit()
                return True

            count, window_start = row
            if current_time - window_start > self.window_seconds:
                conn.execute(
                    "UPDATE limits SET count = ?, window_start = ? WHERE user_id = ?",
                    (1, current_time, user_id),
                )
                conn.commit()
                return True

            if count >= self.limit:
                return False

            conn.execute(
                "UPDATE limits SET count = count + 1 WHERE user_id = ?",
                (user_id,),
            )
            conn.commit()
            return True
