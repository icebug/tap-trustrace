"""REST client handling, including trustraceStream base class."""

import requests
import json

from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class trustraceStream(RESTStream):
    """trustrace stream class."""

    url_base = "https://developer.trustrace.com/api/v2"

    current_page_token_jsonpath = "$.metaData.pageNumber"
    total_pages_jsonpath = "$.metaData.totalPages"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self, key="x-api-key", value=self.config.get("api_key"), location="header"
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if not previous_token:
            current_page_match = extract_jsonpath(
                self.current_page_token_jsonpath, response.json()
            )
            current_page_token = next(iter(current_page_match), None)
        else:
            current_page_token = previous_token

        total_pages_match = extract_jsonpath(
            self.total_pages_jsonpath, response.json()
        )
        total_pages = next(iter(total_pages_match), None)

        if current_page_token and current_page_token < total_pages:
            next_page_token = current_page_token + 1
            return next_page_token
        else:
            return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def prepare_request_payload(
        self, context: Optional[dict], page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """
        if not page_token:
            page_token = 1

        payload = {
            "pagination": {"page": page_token, "size": 100},
            "projection": "detailedView"
        }
        return payload

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records if API changes to need this.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        row["extraction_date"] = date.today().strftime("%Y-%m-%d")
        return row
