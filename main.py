from cosmos.client import CosmosClient
from db.database import get_db
from db.schema import init_schema

from sync.domains import sync_domains
from sync.subdomains import sync_subdomains
from sync.dns_records import sync_dns_records
from sync.networks import sync_networks
from sync.ip_services import sync_ip_services
from sync.hostname_services import sync_hostname_services
from sync.findings import sync_findings


def main():
    client = CosmosClient()
    conn = get_db()
    init_schema(conn)

    print("Domains changed:", sync_domains(conn, client.get_domains()))
    print("Subdomains changed:", sync_subdomains(conn, client.get_subdomains()))
    print("DNS records changed:", sync_dns_records(conn, client.get_dns_records()))
    print("Networks changed:", sync_networks(conn, client.get_networks()))
    print("IP services changed:", sync_ip_services(conn, client.get_ip_services()))
    print("Hostname services changed:", sync_hostname_services(conn, client.get_hostname_services()))
    print("Findings synced:", sync_findings(conn, client.get_findings()))

    conn.close()


if __name__ == "__main__":
    main()