"""
netbox_client.py

Shared NetBox API client used by multiple scripts.

Responsibilities:
- Handle authentication and session setup
- Provide reusable methods for NetBox API interactions
- Centralize error handling and request logic

Configuration is provided via environment variables:
- NETBOX_URL
- NETBOX_API_TOKEN
"""

import os
import requests
from requests.exceptions import RequestException

# Read required configuration from environment variables
NETBOX_URL = os.getenv("NETBOX_URL")
NETBOX_API_TOKEN = os.getenv("NETBOX_API_TOKEN")

if not NETBOX_URL or not NETBOX_API_TOKEN:
    raise RuntimeError("NETBOX_URL and NETBOX_API_TOKEN must be set")

# Common headers used for all NetBox API requests
HEADERS = {
    "Authorization": f"Token {NETBOX_API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class NetBoxClient:
    """
    Lightweight NetBox REST API client.

    This class encapsulates common NetBox API operations and provides
    a clean interface for higher-level scripts.
    """

    def __init__(self):
        """Initialize an HTTP session with shared headers."""
        self.base_url = NETBOX_URL.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _request(self, method, endpoint, **kwargs):
        """
        Perform an HTTP request against the NetBox API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            **kwargs: Additional arguments passed to requests

        Returns:
            dict: Parsed JSON response

        Raises:
            RuntimeError: On HTTP or network errors
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as exc:
            raise RuntimeError(f"NetBox API request failed: {exc}")

    def list_sites(self):
        """
        Retrieve all sites from NetBox.

        Returns:
            dict: API response containing site records
        """
        return self._request("GET", "/api/dcim/sites/")

    def get_site_by_name(self, name):
        """
        Retrieve a site by name.

        Args:
            name (str): Site name to search for

        Returns:
            dict | None: Site object if found, otherwise None
        """
        result = self._request(
            "GET",
            "/api/dcim/sites/",
            params={"name": name},
        )
        return result["results"][0] if result["count"] > 0 else None

    def create_site(self, name, status, tags):
        """
        Create a new site in NetBox.

        Args:
            name (str): Site name
            status (str): Site status (e.g., planned)
            tags (list): List of tags

        Returns:
            dict: Created site object
        """
        payload = {
            "name": name,
            "slug": name.lower().replace("_", "-"),
            "status": status,
            "tags": tags,
        }
        return self._request("POST", "/api/dcim/sites/", json=payload)
