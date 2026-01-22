import json
from db.sync_state import get_last_sync, update_last_sync

_SQL = """
INSERT INTO dns_records (id, hostname, record_type, value, updated_at, raw_json)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    hostname=excluded.hostname,
    record_type=excluded.record_type,
    value=excluded.value,
    updated_at=excluded.updated_at,
    raw_json=excluded.raw_json
WHERE excluded.updated_at > dns_records.updated_at
"""

def sync_dns_records(conn, records):
    c = conn.cursor()
    last_seen = get_last_sync(conn, "dns_records")
    max_seen = last_seen

    rows = []

    for r in records:
        updated = int(r.get("updated_at") or 0)
        if updated <= last_seen:
            continue

        rows.append((
            r["id"],
            r.get("hostname"),
            r.get("record_type"),
            r.get("value"),
            updated,
            json.dumps(r),
        ))
        if updated > max_seen:
            max_seen = updated

    if not rows:
        return 0
    
    changes = 0
    check_sql = "SELECT updated_at FROM dns_records WHERE id = ?"
    for row in rows:
        row_id, hostname, record_type, value, updated_at, raw_json = row
        c.execute(check_sql, (row_id,))
        existing = c.fetchone()
        
        if existing is None:
            c.execute(_SQL, row)
            changes += 1
        elif updated_at > existing[0]:
            c.execute(_SQL, row)
            changes += 1
    conn.commit()

    update_last_sync(conn, "dns_records", max_seen)
    return changes
