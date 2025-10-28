# backend/src/services/google/client.py

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class GoogleCseClient:
    """
    A client responsible for making HTTP requests to the Google CSE API.
    """

    BASE_URL: str = "https://www.googleapis.com/customsearch/v1"

    def __init__(self) -> None:
        """
        Initialize the client and its persistent HTTP session.

        Raises:
            RuntimeError: If the GOOGLE_API_KEY or GOOGLE_CX environment
                variables are not set.
        """
        self.api_key: str | None = os.getenv(key="GOOGLE_API_KEY")
        self.cx: str | None = os.getenv(key="GOOGLE_CX")
        if not self.api_key or not self.cx:
            raise RuntimeError("Missing GOOGLE_API_KEY or GOOGLE_CX environment variables.")

        self.session: requests.Session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def search(self, query: str, date_filter: str | None = None) -> list[dict[str, Any]]:
        """
        Perform a single raw HTTP request to the Google CSE API.

        Args:
            query (str): The search query string to execute.
            date_filter (str | None): A date restriction filter
                (e.g. 'qdr:d', 'qdr:w', 'qdr:m'), or None for no restriction.

        Returns:
            list[dict[str, Any]]: The raw list of 'items' from the API response.
            Returns an empty list if no items are found.

        Raises:
            requests.RequestException: If the HTTP request fails due to network
                issues or receives a non-2xx status code.
        """
        params: dict[str, str | int] = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": 10,
        }
        if date_filter:
            mapping: dict[str, str] = {
                "qdr:d": "d1",
                "qdr:w": "w1",
                "qdr:m": "m1",
            }
            date_restrict: str | None = mapping.get(date_filter)
            if date_restrict:
                params["dateRestrict"] = date_restrict

        response: requests.Response = self.session.get(url=self.BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data.get("items", []) or []

