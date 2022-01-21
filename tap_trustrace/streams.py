"""Stream type classes for tap-trustrace."""
import requests

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers.jsonpath import extract_jsonpath


from tap_trustrace.client import trustraceStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class MaterialsStream(trustraceStream):

    name = "materials"
    path = "/materials"
    primary_keys = ["articleUid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "materials.json"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.records_jsonpath = "$.data.materials[*]"
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())


class StylesStream(trustraceStream):

    name = "styles"
    path = "/styles"
    primary_keys = ["styleUid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "styles.json"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.records_jsonpath = "$.data.styles[*]"
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
