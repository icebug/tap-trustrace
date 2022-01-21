"""trustrace tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_trustrace.streams import trustraceStream, MaterialsStream, StylesStream

STREAM_TYPES = [MaterialsStream, StylesStream]


class Taptrustrace(Tap):
    """trustrace tap class."""

    name = "tap-trustrace"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service",
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
