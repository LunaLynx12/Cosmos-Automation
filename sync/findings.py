import json
from db.sync_state import update_last_sync

_SQL = """
INSERT INTO findings (uid, severity, status, updated_at, raw_json)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(uid) DO UPDATE SET
    severity=excluded.severity,
    status=excluded.status,
    updated_at=excluded.updated_at,
    raw_json=excluded.raw_json
"""

def sync_findings(conn, findings):
    c = conn.cursor()

    rows = []
    for f in findings:
        finding_uid = f.get("uid") or f.get("finding_id")
        if not finding_uid:
            continue

        rows.append((
            finding_uid,
            f.get("severity"),
            f.get("status"),
            f.get("updated_at"),
            json.dumps(f),
        ))

    if rows:
        c.executemany(_SQL, rows)
        conn.commit()

    update_last_sync(conn, "findings", len(rows))
    return len(rows)
