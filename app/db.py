import json
import os
import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import Any, Iterable


def get_conn(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ingested_rows (
          id INTEGER PRIMARY KEY,
          source_filename TEXT NOT NULL,
          sheet_name TEXT NULL,
          row_index INTEGER NOT NULL,
          row_hash TEXT NOT NULL,
          row_json TEXT NOT NULL,
          uploaded_at TEXT NOT NULL
        )
        """
    )

    existing_columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(ingested_rows)").fetchall()
    }
    if "row_hash" not in existing_columns:
        conn.execute("ALTER TABLE ingested_rows ADD COLUMN row_hash TEXT NOT NULL DEFAULT ''")
        conn.execute("UPDATE ingested_rows SET row_hash = '' WHERE row_hash IS NULL")

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_ingested_rows_source
        ON ingested_rows (source_filename)
        """
    )
    conn.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS uidx_ingested_rows_dedupe
        ON ingested_rows (source_filename, sheet_name, row_hash)
        """
    )
    conn.commit()


def insert_rows(
    conn: sqlite3.Connection,
    rows: Iterable[dict[str, Any]],
    *,
    source_filename: str,
    sheet_name: str | None = None,
) -> int:
    now_iso = datetime.now(timezone.utc).isoformat()
    payload: list[tuple[str, str | None, int, str, str, str]] = []

    for i, row in enumerate(rows):
        row_json = json.dumps(
            row,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        row_hash = hashlib.sha256(row_json.encode("utf-8")).hexdigest()
        payload.append(
            (
                source_filename,
                sheet_name,
                i,
                row_hash,
                row_json,
                now_iso,
            )
        )

    before = conn.total_changes
    conn.executemany(
        """
        INSERT OR IGNORE INTO ingested_rows
          (source_filename, sheet_name, row_index, row_hash, row_json, uploaded_at)
        VALUES
          (?, ?, ?, ?, ?, ?)
        """,
        payload,
    )
    conn.commit()
    return conn.total_changes - before
