from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class AuditLogger:
    def __init__(self, db_path: str | Path | None = None):
        base_dir = Path(__file__).resolve().parent
        self.db_path = Path(db_path) if db_path else base_dir / "audit.db"
        self._init_db()

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_hash TEXT NOT NULL,
                    sanitized_query TEXT,
                    query_type TEXT,
                    status TEXT NOT NULL,
                    result_hash TEXT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    block_reason TEXT,
                    metadata_json TEXT
                )
                """
            )
            conn.commit()

    def log_success(self, event: dict[str, Any], result: dict[str, Any]) -> None:
        self._log(event, "SUCCESS", result_hash=self._hash(json.dumps(result, sort_keys=True)), metadata=result)

    def log_blocked(self, event: dict[str, Any], reason: str) -> None:
        self._log(event, "BLOCKED", block_reason=reason)

    def log_error(self, event: dict[str, Any], error_message: str) -> None:
        self._log(event, "ERROR", block_reason=error_message)

    def _log(
        self,
        event: dict[str, Any],
        status: str,
        result_hash: str | None = None,
        block_reason: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO audit_log VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self._hash(event.get("original_query", "")),
                    event.get("sanitized_query"),
                    event.get("query_type"),
                    status,
                    result_hash,
                    event.get("user_id", "default_user"),
                    event.get("session_id", "session_1"),
                    event.get("timestamp", time.time()),
                    block_reason,
                    json.dumps(metadata) if metadata is not None else None,
                ),
            )
            conn.commit()

    def _hash(self, text: str | None) -> str | None:
        if not text:
            return None
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
