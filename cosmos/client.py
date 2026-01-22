import time
import requests
from typing import Dict, List, Any, Optional

from cosmos.config import (
    COSMOS_CLIENT_KEY,
    COSMOS_CLIENT_SECRET,
    COSMOS_TOKEN_URL,
    COSMOS_API_URL,
    COSMOS_ORG_ID,
    COSMOS_AUDIENCE,
)


class CosmosClient:
    def __init__(self):
        missing = [
            name for name, val in {
                "cosmos_client_key": COSMOS_CLIENT_KEY,
                "cosmos_client_secret": COSMOS_CLIENT_SECRET,
                "cosmos_token_url": COSMOS_TOKEN_URL,
                "cosmos_api_url": COSMOS_API_URL,
                "cosmos_org_id": COSMOS_ORG_ID,
            }.items()
            if not val
        ]
        if missing:
            raise RuntimeError(f"Missing required Cosmos environment variables: {', '.join(missing)}")

        self.api_key = COSMOS_CLIENT_KEY
        self.api_secret = COSMOS_CLIENT_SECRET
        self.token_url = COSMOS_TOKEN_URL
        self.base_url = COSMOS_API_URL
        self.organization_id = COSMOS_ORG_ID
        self.audience = COSMOS_AUDIENCE
        self.token: Optional[str] = None
        self.token_expiry: float = 0.0
        self.session = requests.Session()

    def authenticate(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "audience": self.audience,
        }

        if self.token_url is None:
            raise ValueError("Token URL is not set.")
        r = self.session.post(self.token_url, data=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        self.token = data["access_token"]
        self.token_expiry = time.time() + data.get("expires_in", 36000) - 60

    def headers(self) -> Dict[str, str]:
        if not self.token or time.time() > self.token_expiry:
            self.authenticate()
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def paginated_get(self, path: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        page = None

        while True:
            q = dict(params)
            if page:
                q["page"] = page

            r = self.session.get(
                f"{self.base_url}{path}",
                headers=self.headers(),
                params=q,
                timeout=60,
            )
            r.raise_for_status()

            data = r.json()
            results.extend(data.get("data", []))
            page = data.get("nextPageToken")
            if not page:
                break

        return results

    def get_domains(self, enabled: Optional[bool] = None):
        params = {"organization_id": self.organization_id, "customer_id": self.organization_id}
        if enabled is not None:
            params["enabled"] = str(enabled).lower()
        return self.paginated_get("/v5/asset-view/domains", params)

    def get_subdomains(self, **filters):
        params = {"organization_id": self.organization_id, "customer_id": self.organization_id, **filters}
        return self.paginated_get("/v5/asset-view/subdomains", params)

    def get_dns_records(self, **filters):
        params = {"organization_id": self.organization_id, "customer_id": self.organization_id, **filters}
        return self.paginated_get("/v5/asset-view/dns-records", params)

    def get_networks(self, **filters):
        params = {"organization_id": self.organization_id, "customer_id": self.organization_id, **filters}
        return self.paginated_get("/v5/asset-view/networks", params)

    def get_ip_services(self, **filters):
        params = {"organization_id": self.organization_id, "customer_id": self.organization_id, **filters}
        return self.paginated_get("/v5/asset-view/ip-services", params)

    def get_hostname_services(self, **filters):
        params = {"organization_id": self.organization_id, "customer_id": self.organization_id, **filters}
        return self.paginated_get("/v5/asset-view/hostname-services", params)

    def get_findings(self, **filters):
        params = {"organization_id": self.organization_id, **filters}
        return self.paginated_get("/v5/findings", params)
