import json
from db.sync_state import get_last_sync, update_last_sync

_SQL = """
INSERT INTO hostname_services (id, hostname, port, application_protocol, updated_at, raw_json)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    hostname=excluded.hostname,
    port=excluded.port,
    application_protocol=excluded.application_protocol,
    updated_at=excluded.updated_at,
    raw_json=excluded.raw_json
WHERE excluded.updated_at > hostname_services.updated_at
"""

def sync_hostname_services(conn, services):
    c = conn.cursor()
    last_seen = get_last_sync(conn, "hostname_services")
    max_seen = last_seen

    rows = []

    for s in services:
        updated = int(s.get("updated_at") or 0)
        if updated <= last_seen:
            continue

        rows.append((
            s["id"],
            s.get("hostname"),
            s.get("port"),
            s.get("application_protocol"),
            updated,
            json.dumps(s),
        ))
        
        if updated > max_seen:
            max_seen = updated

    if not rows:
        return 0

    changes = 0
    check_sql = "SELECT updated_at FROM hostname_services WHERE id = ?"
    for row in rows:
        row_id, hostname, port, application_protocol, updated_at, raw_json = row
        c.execute(check_sql, (row_id,))
        existing = c.fetchone()
        
        if existing is None:
            c.execute(_SQL, row)
            changes += 1
        else:
            existing_updated = existing[0]
            if existing_updated is None:
                existing_updated = 0
            else:
                existing_updated = int(existing_updated)
            
            if updated_at > existing_updated:
                c.execute(_SQL, row)
                changes += 1
    conn.commit()

    update_last_sync(conn, "hostname_services", max_seen)
    return changes