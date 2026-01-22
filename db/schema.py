def init_schema(conn):
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS sync_state (
        asset_type TEXT PRIMARY KEY,
        last_updated_at INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS domains (
        id TEXT PRIMARY KEY,
        domain TEXT,
        enabled INTEGER,
        updated_at INTEGER,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS subdomains (
        id TEXT PRIMARY KEY,
        hostname TEXT,
        enabled INTEGER,
        updated_at INTEGER,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS dns_records (
        id TEXT PRIMARY KEY,
        hostname TEXT,
        record_type TEXT,
        value TEXT,
        updated_at INTEGER,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS networks (
        id TEXT PRIMARY KEY,
        address TEXT,
        prefix INTEGER,
        updated_at INTEGER,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ip_services (
        id TEXT PRIMARY KEY,
        ip_address TEXT,
        port INTEGER,
        application_protocol TEXT,
        updated_at INTEGER,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS hostname_services (
        id TEXT PRIMARY KEY,
        hostname TEXT,
        port INTEGER,
        application_protocol TEXT,
        updated_at INTEGER,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        uid TEXT PRIMARY KEY,
        severity TEXT,
        status TEXT,
        updated_at TEXT,
        raw_json TEXT
    )
    """)

    c.execute("CREATE INDEX IF NOT EXISTS idx_domains_updated ON domains(updated_at)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_subdomains_updated ON subdomains(updated_at)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_dns_hostname ON dns_records(hostname)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_networks_address ON networks(address)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_ip_services_ip ON ip_services(ip_address)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_hostname_services_hostname ON hostname_services(hostname)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity)")

    conn.commit()