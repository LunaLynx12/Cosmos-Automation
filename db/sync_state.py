import sqlite3

def get_last_sync(conn: sqlite3.Connection, asset_type: str) -> int:
    c = conn.cursor()
    c.execute("SELECT last_updated_at FROM sync_state WHERE asset_type = ?", (asset_type,))
    row = c.fetchone()
    return int(row[0]) if row and row[0] is not None else 0

def update_last_sync(conn: sqlite3.Connection, asset_type: str, value: int) -> None:
    c = conn.cursor()
    c.execute("""
        INSERT INTO sync_state (asset_type, last_updated_at)
        VALUES (?, ?)
        ON CONFLICT(asset_type) DO UPDATE SET
            last_updated_at = CASE
                WHEN excluded.last_updated_at > sync_state.last_updated_at
                THEN excluded.last_updated_at
                ELSE sync_state.last_updated_at
            END
    """, (asset_type, int(value)))
    conn.commit()