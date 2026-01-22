import os
import dotenv

dotenv.load_dotenv()

COSMOS_CLIENT_KEY = os.getenv("cosmos_client_key")
COSMOS_CLIENT_SECRET = os.getenv("cosmos_client_secret")
COSMOS_TOKEN_URL = os.getenv("cosmos_token_url")
COSMOS_API_URL = os.getenv("cosmos_api_url")
COSMOS_ORG_ID = os.getenv("cosmos_org_id")
COSMOS_AUDIENCE = os.getenv("cosmos_audience", "cosmos_public")