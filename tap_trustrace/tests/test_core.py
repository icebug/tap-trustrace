"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests

from tap_trustrace.tap import Taptrustrace

SAMPLE_CONFIG = {
    "api_key": "b4c5edf8-61e6856626e5-57625af52cee-d7eb85d9840f",
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(Taptrustrace, config=SAMPLE_CONFIG)
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
