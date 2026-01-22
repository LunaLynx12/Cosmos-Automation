import json
from db.sync_state import get_last_sync, update_last_sync

_SQL = """
INSERT INTO domains (id, domain, enabled, updated_at, raw_json)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    domain=excluded.domain,
    enabled=excluded.enabled,
    updated_at=excluded.updated_at,
    raw_json=excluded.raw_json
WHERE excluded.updated_at > domains.updated_at
"""

def sync_domains(conn, domains):
    c = conn.cursor()
    last_seen = get_last_sync(conn, "domains")
    max_seen = last_seen

    rows = []

    for d in domains:
        updated = int(d.get("updated_at") or 0)
        if updated <= last_seen:
            continue

        rows.append((
            d["id"],
            d.get("domain"),
            int(d.get("enabled", False)),
            updated,
            json.dumps(d),
        ))
        if updated > max_seen:
            max_seen = updated

    if not rows:
        return 0

    changes = 0
    check_sql = "SELECT updated_at FROM domains WHERE id = ?"
    for row in rows:
        row_id, domain, enabled, updated_at, raw_json = row
        c.execute(check_sql, (row_id,))
        existing = c.fetchone()
        
        if existing is None:
            c.execute(_SQL, row)
            changes += 1
        elif updated_at > existing[0]:
            c.execute(_SQL, row)
            changes += 1
    conn.commit()

    update_last_sync(conn, "domains", max_seen)
    return changes
