import json
from db.sync_state import get_last_sync, update_last_sync

_SQL = """
INSERT INTO subdomains (id, hostname, enabled, updated_at, raw_json)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    hostname=excluded.hostname,
    enabled=excluded.enabled,
    updated_at=excluded.updated_at,
    raw_json=excluded.raw_json
WHERE excluded.updated_at > subdomains.updated_at
"""

def sync_subdomains(conn, subs):
    c = conn.cursor()
    last_seen = get_last_sync(conn, "subdomains")
    max_seen = last_seen

    rows = []

    for s in subs:
        updated = int(s.get("updated_at") or 0)
        if updated <= last_seen:
            continue

        rows.append((
            s["id"],
            s.get("hostname"),
            int(s.get("enabled", False)),
            updated,
            json.dumps(s),
        ))

        if updated > max_seen:
            max_seen = updated

    if not rows:
        return 0

    changes = 0
    check_sql = "SELECT updated_at FROM subdomains WHERE id = ?"
    for row in rows:
        row_id, hostname, enabled, updated_at, raw_json = row
        c.execute(check_sql, (row_id,))
        existing = c.fetchone()
        
        if existing is None:
            c.execute(_SQL, row)
            changes += 1
        elif updated_at > existing[0]:
            c.execute(_SQL, row)
            changes += 1
    conn.commit()

    update_last_sync(conn, "subdomains", max_seen)
    return changes
