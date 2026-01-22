import json
from db.sync_state import get_last_sync, update_last_sync

_SQL = """
INSERT INTO networks (id, address, prefix, updated_at, raw_json)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    address=excluded.address,
    prefix=excluded.prefix,
    updated_at=excluded.updated_at,
    raw_json=excluded.raw_json
WHERE excluded.updated_at > networks.updated_at
"""

def sync_networks(conn, networks):
    c = conn.cursor()
    last_seen = get_last_sync(conn, "networks")
    max_seen = last_seen

    rows = []

    for n in networks:
        updated = int(n.get("updated_at") or 0)
        if updated <= last_seen:
            continue

        rows.append((
            n["id"],
            n.get("address"),
            n.get("prefix"),
            updated,
            json.dumps(n),
        ))

        if updated > max_seen:
            max_seen = updated

    if not rows:
        return 0

    changes = 0
    check_sql = "SELECT updated_at FROM networks WHERE id = ?"
    for row in rows:
        row_id, address, prefix, updated_at, raw_json = row
        c.execute(check_sql, (row_id,))
        existing = c.fetchone()
        
        if existing is None:
            c.execute(_SQL, row)
            changes += 1
        elif updated_at > existing[0]:
            c.execute(_SQL, row)
            changes += 1
    conn.commit()

    update_last_sync(conn, "networks", max_seen)
    return changes
