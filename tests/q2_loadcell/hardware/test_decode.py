from __future__ import annotations

import pytest

from q2_loadcell.hardware.decode import decode_sample


class TestDecode:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.negative_payload = b"\x1b\xd1\xeb\x00"
        self.positive_payload = b"\x10\x27\x00\x00"
        self.trailing_byte_payload = b"\x01\x00\x00\x7f"

    def test_decode_sample_WHEN_24bit_negative_EXPECT_signed_value(self):
        expected = -1322725

        actual = decode_sample(self.negative_payload)

        assert actual == expected

    def test_decode_sample_WHEN_positive_EXPECT_positive_value(self):
        expected = 10000

        actual = decode_sample(self.positive_payload)

        assert actual == expected

    def test_decode_sample_WHEN_trailing_byte_set_EXPECT_trailing_byte_ignored(self):
        expected = 1

        actual = decode_sample(self.trailing_byte_payload)

        assert actual == expected
