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
            method (str): HTTP method (GET, POST, DELETE, etc.)
            endpoint (str): API endpoint path
            **kwargs: Additional arguments passed to requests

        Returns:
            dict | None: Parsed JSON response or None for 204 responses

        Raises:
            RuntimeError: On HTTP or network errors
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()

            # NetBox DELETE returns 204 No Content
            if response.status_code == 204:
                return None

            return response.json()
        
        except RequestException as exc:
            if exc.response is not None:
                raise RuntimeError(
                    f"NetBox API error {exc.response.status_code}: {exc.response.text}"
                )
    
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

    def get_tag_by_name(self, name):
        """
        Retrieve a tag by name.

        Args:
            name (str): Tag name

        Returns:
            dict | None: Tag object if found
        """  
        result = self._request(
            "GET",
            "/api/extras/tags/",
            params={"name": name},
        )
        return result["results"][0] if result["count"] > 0 else None

    def create_tag(self, name):
        """
        Create a tag if it does not exist.

        Args:
            name (str): Tag name

        Returns:
            dict: Created tag object
        """
        payload = {
            "name": name,
            "slug": name.lower().replace("_", "-"),
        }
        return self._request("POST", "/api/extras/tags/", json=payload)

    def create_site(self, name, status="planned", tags=None):
        """
        Create a new site in NetBox.

        Args:
            name (str): Site name
            status (str): Site status slug (e.g. planned, active)
            tags (list[str]): Optional list of tag names

        Returns:
            dict: Created site object
        """
        payload = {
            "name": name,
            "slug": name.lower().replace("_", "-"),
            "status": status,
        }

        if tags:
            tag_objects = []
            for tag in tags:
                tag_obj = self.get_tag_by_name(tag)
                if not tag_obj:
                    tag_obj = self.create_tag(tag)
                tag_objects.append(tag_obj["id"])

            payload["tags"] = tag_objects

        return self._request("POST", "/api/dcim/sites/", json=payload)

    def delete_site(self, name):
        """
        Delete a site from NetBox by name.

        Args:
            name (str): Site name to delete

        Returns:
            bool: True if deleted, False if site not found
        """
        site = self.get_site_by_name(name)
        if not site:
            return False

        site_id = site["id"]
        self._request("DELETE", f"/api/dcim/sites/{site_id}/")
        return True