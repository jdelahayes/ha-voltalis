"""aoivoltalis constants."""
from enum import Enum


# HTTP METHOD
class HTTPMethod(Enum):
    """HTTPMethod Enum."""

    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"


# URL
BASE_URL = "https://api.myvoltalis.com"
LOGIN_URL = BASE_URL + "/auth/login"
LOGOUT_URL = BASE_URL + "/auth/logout"
ACCOUNT_ME_URL = BASE_URL + "/api/account/me"
APPLIANCE_URL = BASE_URL + "/api/site/__site__/managed-appliance"
MANUAL_SETTING_URL = BASE_URL + "/api/site/__site__/manualsetting"
PROGRAMMING_PROGRAMS_URL = BASE_URL + "/api/site/__site__/programming/program"
PROGRAMMING_PROGRAM_URL = BASE_URL + "/api/site/__site__/programming/program/__program__"
PROGRAMMING_STATE_URL = BASE_URL + "/api/site/__site__/programming/state"

# Cache
AUTH_TOKEN = "auth_token"
DEFAULT_SITE_ID = "default_site_id"
