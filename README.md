# Cosmos Automation

A Python automation tool for syncing asset data from the Cosmos API to a local SQLite database. This tool keeps your local database up-to-date with domains, subdomains, DNS records, networks, IP services, hostname services, and findings from Cosmos.

## Features

- **Incremental Sync**: Only syncs data that has changed since the last sync, using timestamp-based filtering
- **Multiple Asset Types**: Syncs domains, subdomains, DNS records, networks, IP services, hostname services, and findings
- **Efficient Updates**: Uses SQLite's `ON CONFLICT` to handle inserts and updates efficiently
- **Change Tracking**: Reports the number of actual changes made during each sync

## Requirements

- Python 3.8+
- Cosmos API credentials

## Installation

1. Clone this repository:
```bash
git clone https://github.com/LunaLynx12/Cosmos-Automation.git
cd "Cosmos Automation"
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following environment variables:

```env
cosmos_client_key=your_client_key
cosmos_client_secret=your_client_secret
cosmos_token_url=your_token_url
cosmos_api_url=your_api_url
cosmos_org_id=your_organization_id
cosmos_audience=cosmos_public
```

## Usage

Run the sync script:

```bash
python main.py
```

The script will:
1. Connect to the Cosmos API
2. Fetch all asset data
3. Sync only changed records to the local SQLite database
4. Display the number of changes made for each asset type

Example output:
```
Domains changed: 0
Subdomains changed: 0
DNS records changed: 0
Networks changed: 0
IP services changed: 0
Hostname services changed: 0
Findings synced: 137
```

## Database

The database is stored in `data/cosmos.db` by default. The schema includes tables for:
- `domains` - Domain information
- `subdomains` - Subdomain records
- `dns_records` - DNS record entries
- `networks` - Network information
- `ip_services` - IP-based services
- `hostname_services` - Hostname-based services
- `findings` - Security findings
- `sync_state` - Tracks the last sync timestamp for each asset type

## Project Structure

```
.
├── cosmos/          # Cosmos API client
│   ├── client.py    # API client implementation
│   └── config.py    # Configuration management
├── db/              # Database layer
│   ├── database.py  # Database connection
│   ├── schema.py    # Schema initialization
│   └── sync_state.py # Sync state tracking
├── sync/            # Sync modules for each asset type
│   ├── domains.py
│   ├── subdomains.py
│   ├── dns_records.py
│   ├── networks.py
│   ├── ip_services.py
│   ├── hostname_services.py
│   └── findings.py
├── utils/           # Utility functions
├── data/            # Database storage directory
├── main.py          # Main entry point
└── requirements.txt # Python dependencies
```

## How It Works

1. **Authentication**: The client authenticates with Cosmos API using OAuth2 client credentials
2. **Data Fetching**: Each asset type is fetched using paginated API requests
3. **Change Detection**: Only records with `updated_at` timestamps greater than the last sync are processed
4. **Database Updates**: Records are inserted or updated using SQLite's `ON CONFLICT` clause with timestamp comparison
5. **State Tracking**: After each sync, the maximum `updated_at` timestamp is saved to prevent re-processing the same data

## Notes

- The database is automatically created on first run
- The sync process is idempotent - running it multiple times will only process new or updated records
- All raw JSON data from the API is stored in the `raw_json` column for each table
