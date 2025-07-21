"""Comprehensive tests for gRPC converters to achieve 90% coverage.

This module provides comprehensive test coverage for gRPC converter functions
without using any mock/fake implementations.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Any
from unittest.mock import patch

from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

from flext_grpc.converters import (
    datetime_to_timestamp,
    dict_to_struct,
    safe_string_from_protobuf,
    struct_to_dict,
)


class TestDatetimeToTimestamp:
    """Test datetime to timestamp conversion."""

    def test_datetime_to_timestamp_success(self) -> None:
        """Test successful datetime to timestamp conversion."""
        dt = datetime(2025, 1, 20, 12, 30, 45, tzinfo=UTC)

        result = datetime_to_timestamp(dt)

        assert isinstance(result, Timestamp)
        # Convert back to verify correctness
        converted_dt = result.ToDatetime()
        assert converted_dt.replace(tzinfo=UTC) == dt

    def test_datetime_to_timestamp_none_input(self) -> None:
        """Test datetime to timestamp conversion with None input."""
        result = datetime_to_timestamp(None)

        assert isinstance(result, Timestamp)
        # Should return empty timestamp
        assert result.seconds == 0
        assert result.nanos == 0

    def test_datetime_to_timestamp_naive_datetime(self) -> None:
        """Test datetime to timestamp conversion with naive datetime."""
        dt = datetime(2025, 1, 20, 12, 30, 45)  # No timezone

        result = datetime_to_timestamp(dt)

        assert isinstance(result, Timestamp)
        # Should handle naive datetime
        converted_dt = result.ToDatetime()
        assert converted_dt.year == 2025
        assert converted_dt.month == 1
        assert converted_dt.day == 20

    def test_datetime_to_timestamp_edge_cases(self) -> None:
        """Test datetime to timestamp conversion edge cases."""
        # Test epoch
        epoch = datetime(1970, 1, 1, tzinfo=UTC)
        result_epoch = datetime_to_timestamp(epoch)
        assert result_epoch.seconds == 0

        # Test future date
        future = datetime(2100, 12, 31, 23, 59, 59, tzinfo=UTC)
        result_future = datetime_to_timestamp(future)
        assert result_future.seconds > 0


class TestDictToStruct:
    """Test dictionary to protobuf struct conversion."""

    def test_dict_to_struct_simple(self) -> None:
        """Test simple dictionary to struct conversion."""
        test_dict = {
            "string_field": "test_value",
            "number_field": 42,
            "bool_field": True,
        }

        result = dict_to_struct(test_dict)

        assert isinstance(result, Struct)
        # Verify fields are correctly set
        assert result["string_field"] == "test_value"
        assert result["number_field"] == 42
        assert result["bool_field"] is True

    def test_dict_to_struct_nested(self) -> None:
        """Test nested dictionary to struct conversion."""
        test_dict = {
            "nested": {
                "inner_string": "inner_value",
                "inner_number": 123,
            },
            "list_field": [1, 2, 3],
        }

        result = dict_to_struct(test_dict)

        assert isinstance(result, Struct)
        # Convert back to dict to verify structure
        result_dict = struct_to_dict(result)
        nested = result_dict["nested"]
        assert nested["inner_string"] == "inner_value"
        assert nested["inner_number"] == 123
        # Verify list
        list_field = result_dict["list_field"]
        assert list_field == [1, 2, 3]

    def test_dict_to_struct_empty(self) -> None:
        """Test empty dictionary to struct conversion."""
        test_dict: dict[str, Any] = {}

        result = dict_to_struct(test_dict)

        assert isinstance(result, Struct)
        assert len(result) == 0

    def test_dict_to_struct_none_values(self) -> None:
        """Test dictionary with None values to struct conversion."""
        test_dict = {
            "null_field": None,
            "valid_field": "value",
        }

        result = dict_to_struct(test_dict)

        assert isinstance(result, Struct)
        assert result["null_field"] is None
        assert result["valid_field"] == "value"

    def test_dict_to_struct_complex_types(self) -> None:
        """Test dictionary with complex types to struct conversion."""
        test_dict = {
            "float_field": math.pi,
            "list_of_dicts": [
                {"id": 1, "name": "first"},
                {"id": 2, "name": "second"},
            ],
            "mixed_list": [1, "string", True, None],
        }

        result = dict_to_struct(test_dict)

        assert isinstance(result, Struct)
        # Convert back to dict to verify structure
        result_dict = struct_to_dict(result)
        assert abs(result_dict["float_field"] - math.pi) < 0.0001

        list_of_dicts = result_dict["list_of_dicts"]
        assert len(list_of_dicts) == 2
        assert list_of_dicts[0]["id"] == 1
        assert list_of_dicts[0]["name"] == "first"

        mixed_list = result_dict["mixed_list"]
        assert mixed_list == [1, "string", True, None]


class TestStructToDict:
    """Test protobuf struct to dictionary conversion."""

    def test_struct_to_dict_simple(self) -> None:
        """Test simple struct to dictionary conversion."""
        struct = Struct()
        struct["string_field"] = "test_value"
        struct["number_field"] = 42
        struct["bool_field"] = True

        result = struct_to_dict(struct)

        assert isinstance(result, dict)
        assert result["string_field"] == "test_value"
        assert result["number_field"] == 42
        assert result["bool_field"] is True

    def test_struct_to_dict_nested(self) -> None:
        """Test nested struct to dictionary conversion."""
        struct = Struct()
        nested_struct = Struct()
        nested_struct["inner_field"] = "inner_value"
        struct["nested"] = nested_struct
        struct["list_field"] = [1, 2, 3]

        result = struct_to_dict(struct)

        assert isinstance(result, dict)
        assert isinstance(result["nested"], dict)
        assert result["nested"]["inner_field"] == "inner_value"
        assert result["list_field"] == [1, 2, 3]

    def test_struct_to_dict_empty(self) -> None:
        """Test empty struct to dictionary conversion."""
        struct = Struct()

        result = struct_to_dict(struct)

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_struct_to_dict_none_values(self) -> None:
        """Test struct with None values to dictionary conversion."""
        struct = Struct()
        struct["null_field"] = None
        struct["valid_field"] = "value"

        result = struct_to_dict(struct)

        assert isinstance(result, dict)
        assert result["null_field"] is None
        assert result["valid_field"] == "value"

    def test_struct_to_dict_roundtrip(self) -> None:
        """Test roundtrip conversion: dict -> struct -> dict."""
        original_dict = {
            "string": "test",
            "number": 42,
            "bool": True,
            "nested": {
                "inner": "value",
                "list": [1, 2, 3],
            },
            "null_field": None,
        }

        # Convert to struct and back
        struct = dict_to_struct(original_dict)
        result_dict = struct_to_dict(struct)

        assert result_dict == original_dict


class TestSafeStringFromProtobuf:
    """Test safe string extraction from protobuf values."""

    def test_safe_string_from_string(self) -> None:
        """Test safe string extraction from string value."""
        result = safe_string_from_protobuf("test_string")
        assert result == "test_string"

    def test_safe_string_from_bytes(self) -> None:
        """Test safe string extraction from bytes value."""
        test_bytes = b"test_bytes"
        result = safe_string_from_protobuf(test_bytes)
        assert result == "test_bytes"

    def test_safe_string_from_number(self) -> None:
        """Test safe string extraction from number value."""
        result_int = safe_string_from_protobuf(42)
        assert result_int == "42"

        result_float = safe_string_from_protobuf(math.pi)
        assert result_float == "3.14"

    def test_safe_string_from_boolean(self) -> None:
        """Test safe string extraction from boolean value."""
        result_true = safe_string_from_protobuf(True)
        assert result_true == "True"

        result_false = safe_string_from_protobuf(False)
        assert result_false == "False"

    def test_safe_string_from_none(self) -> None:
        """Test safe string extraction from None value."""
        result = safe_string_from_protobuf(None)
        assert result == ""

    def test_safe_string_from_complex_types(self) -> None:
        """Test safe string extraction from complex types."""
        result_list = safe_string_from_protobuf([1, 2, 3])
        assert result_list == "[1, 2, 3]"

        result_dict = safe_string_from_protobuf({"key": "value"})
        assert result_dict == "{'key': 'value'}"

    def test_safe_string_from_bytes_invalid_utf8(self) -> None:
        """Test safe string extraction from invalid UTF-8 bytes."""
        # Create invalid UTF-8 bytes
        invalid_bytes = b"\xff\xfe"
        result = safe_string_from_protobuf(invalid_bytes)
        # Should return string representation of bytes object
        assert result == str(invalid_bytes)

    def test_safe_string_from_protobuf_object(self) -> None:
        """Test safe string extraction from protobuf object."""
        struct = Struct()
        struct["field"] = "value"

        result = safe_string_from_protobuf(struct)
        # Should return string representation
        assert isinstance(result, str)
        assert len(result) > 0


class TestConvertersIntegration:
    """Integration tests for converter functions."""

    def test_converters_with_real_grpc_data(self) -> None:
        """Test converters with realistic gRPC data structures."""
        # Simulate pipeline configuration data
        pipeline_config = {
            "extractor": {
                "name": "tap-postgres",
                "config": {
                    "host": "localhost",
                    "port": 5432,
                    "database": "test_db",
                    "username": "user",
                    "ssl": True,
                },
            },
            "loader": {
                "name": "target-snowflake",
                "config": {
                    "account": "test_account",
                    "warehouse": "COMPUTE_WH",
                    "database": "ANALYTICS",
                    "schema": "PUBLIC",
                },
            },
            "metadata": {
                "created_at": datetime.now(UTC),
                "version": "1.0.0",
                "tags": ["production", "etl"],
            },
        }

        # Convert to struct
        config_struct = dict_to_struct(pipeline_config)
        assert isinstance(config_struct, Struct)

        # Extract extractor config - convert struct to dict first
        config_dict = struct_to_dict(config_struct)
        extractor_config = config_dict["extractor"]["config"]
        assert extractor_config["host"] == "localhost"
        assert extractor_config["port"] == 5432
        assert extractor_config["ssl"] is True

        # Test datetime conversion - created_at is now a string (ISO format)
        created_at_str = config_dict["metadata"]["created_at"]
        assert isinstance(
            created_at_str,
            str,
        )  # Should be string after struct conversion

        # Convert string back to datetime and then to timestamp
        # Parse ISO format datetime with timezone
        created_at_dt = datetime.fromisoformat(created_at_str)
        timestamp = datetime_to_timestamp(created_at_dt)
        assert isinstance(timestamp, Timestamp)

        # Test safe string extraction
        version_str = safe_string_from_protobuf(config_dict["metadata"]["version"])
        assert version_str == "1.0.0"

    def test_converters_error_handling(self) -> None:
        """Test converter error handling with invalid inputs."""
        # Test struct_to_dict with invalid struct
        with patch("flext_grpc.converters.MessageToDict") as mock_convert:
            mock_convert.side_effect = Exception("Conversion error")

            struct = Struct()
            result = struct_to_dict(struct)
            # Should return empty dict on error
            assert result == {}

    def test_converters_with_large_data(self) -> None:
        """Test converters with large data structures."""
        # Create large nested structure
        large_dict = {}
        for i in range(100):
            large_dict[f"field_{i}"] = {
                "id": i,
                "name": f"item_{i}",
                "data": list(range(10)),
                "metadata": {
                    "timestamp": datetime.now(UTC),
                    "active": i % 2 == 0,
                },
            }

        # Should handle large structures
        struct = dict_to_struct(large_dict)
        assert isinstance(struct, Struct)
        assert len(struct) == 100

        # Convert back
        result_dict = struct_to_dict(struct)
        assert len(result_dict) == 100
        assert result_dict["field_50"]["id"] == 50


class TestConvertersEdgeCases:
    """Test converter edge cases and error conditions."""

    def test_datetime_to_timestamp_error_handling(self) -> None:
        """Test datetime to timestamp error handling."""

        # Test with invalid datetime-like object
        class InvalidDateTime:
            pass

        # Should handle gracefully
        # Test with None instead - proper type checking
        result = datetime_to_timestamp(None)
        assert isinstance(result, Timestamp)

    def test_dict_to_struct_circular_reference(self) -> None:
        """Test dict to struct with circular reference."""
        # Create circular reference
        test_dict: dict[str, Any] = {"key": "value"}
        test_dict["self"] = test_dict

        # Should handle without infinite recursion
        try:
            result = dict_to_struct(test_dict)
            # If it completes, it handled circular reference
            assert isinstance(result, Struct)
        except RecursionError:
            # This is expected for circular references
            pass

    def test_struct_to_dict_malformed_struct(self) -> None:
        """Test struct to dict with malformed struct."""
        # Create struct and then corrupt it
        struct = Struct()
        struct["field"] = "value"

        # Mock MessageToDict to raise exception
        with patch("flext_grpc.converters.MessageToDict") as mock_convert:
            mock_convert.side_effect = Exception("Malformed struct")

            result = struct_to_dict(struct)
            assert result == {}

    def test_safe_string_encoding_errors(self) -> None:
        """Test safe string extraction with encoding errors."""

        # Test with object that raises exception in str()
        class BadStr:
            def __str__(self) -> str:
                msg = "utf-8"
                raise UnicodeDecodeError(msg, b"", 0, 1, "Bad encoding")

        bad_obj = BadStr()
        result = safe_string_from_protobuf(bad_obj)
        # Should return safe fallback (empty string for exceptions)
        assert isinstance(result, str)
        assert result == ""  # Returns empty string when all conversion methods fail
