"""Tests for Protocol Buffer utility functions."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Never

import pytest
from google.protobuf import struct_pb2, timestamp_pb2

from flext_grpc.converters import (
    datetime_to_timestamp,
    dict_to_struct,
    safe_string_from_protobuf,
    struct_to_dict,
)


class TestDatetimeToTimestamp:
    """Test datetime to protobuf Timestamp conversion."""

    def test_datetime_to_timestamp_with_datetime(self) -> None:
        """Test conversion from datetime object."""
        dt = datetime(2025, 1, 20, 12, 0, 0, tzinfo=UTC)
        result = datetime_to_timestamp(dt)
        assert isinstance(result, timestamp_pb2.Timestamp)
        assert result.seconds > 0
        assert result.nanos >= 0

    def test_datetime_to_timestamp_with_iso_string(self) -> None:
        """Test conversion from ISO format string."""
        iso_string = "2025-01-20T12:00:00+00:00"
        result = datetime_to_timestamp(iso_string)
        assert isinstance(result, timestamp_pb2.Timestamp)
        assert result.seconds > 0

    def test_datetime_to_timestamp_with_iso_string_no_timezone(self) -> None:
        """Test conversion from ISO format string without timezone."""
        iso_string = "2025-01-20T12:00:00"
        result = datetime_to_timestamp(iso_string)
        assert isinstance(result, timestamp_pb2.Timestamp)
        assert result.seconds > 0

    def test_datetime_to_timestamp_with_none(self) -> None:
        """Test conversion with None input."""
        result = datetime_to_timestamp(None)
        assert isinstance(result, timestamp_pb2.Timestamp)
        assert result.seconds == 0
        assert result.nanos == 0

    def test_datetime_to_timestamp_with_malformed_string(self) -> None:
        """Test conversion with malformed ISO string."""
        with pytest.raises(ValueError, match="Invalid isoformat string"):
            datetime_to_timestamp("not-a-date")


class TestDictToStruct:
    """Test dictionary to protobuf Struct conversion."""

    def test_dict_to_struct_simple_dict(self) -> None:
        """Test conversion of simple dictionary."""
        data = {"key": "value", "number": 42, "boolean": True}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        assert "key" in result
        assert "number" in result
        assert "boolean" in result
        # Verify we can convert back to dict and get original values
        converted_back = struct_to_dict(result)
        assert converted_back["key"] == "value"
        assert converted_back["number"] == 42
        assert converted_back["boolean"] is True

    def test_dict_to_struct_nested_dict(self) -> None:
        """Test conversion of nested dictionary."""
        data = {"outer": {"inner": "value", "nested_number": 123}, "top_level": "test"}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        assert "outer" in result
        assert "top_level" in result

    def test_dict_to_struct_with_datetime(self) -> None:
        """Test conversion with datetime objects."""
        dt = datetime(2025, 1, 20, 12, 0, 0, tzinfo=UTC)
        data = {"created_at": dt, "name": "test"}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        assert "created_at" in result
        assert "name" in result

    def test_dict_to_struct_with_list(self) -> None:
        """Test conversion with list values."""
        data = {"items": ["item1", "item2", "item3"], "numbers": [1, 2, 3]}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        assert "items" in result
        assert "numbers" in result

    def test_dict_to_struct_with_object(self) -> None:
        """Test conversion with custom object having __dict__."""
        class TestObject:
            def __init__(self) -> None:
                self.name = "test"
                self.value = 42
        obj = TestObject()
        data = {"object": obj}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        assert "object" in result

    def test_dict_to_struct_with_non_json_serializable(self) -> None:
        """Test conversion with non-JSON serializable values."""
        class NonSerializable:
            def __str__(self) -> str:
                return "non-serializable"
        data = {"item": NonSerializable()}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        # Should convert to string representation

    def test_dict_to_struct_empty_dict(self) -> None:
        """Test conversion of empty dictionary."""
        data: dict[str, Any] = {}
        result = dict_to_struct(data)
        assert isinstance(result, struct_pb2.Struct)
        assert len(result) == 0

    def test_dict_to_struct_none_data(self) -> None:
        """Test conversion with None data."""
        result = dict_to_struct(None)
        assert isinstance(result, struct_pb2.Struct)
        assert len(result) == 0

    def test_dict_to_struct_conversion_failure(self) -> None:
        """Test handling of conversion failures."""
        # Create a problematic data structure that might cause issues
        data = {"key": "value"}
        # Mock struct.update to raise an exception
        original_update = struct_pb2.Struct.update

        def mock_update(self: struct_pb2.Struct, data: dict[str, Any]) -> Never:
            msg = "Conversion failed"
            raise ValueError(msg)
        struct_pb2.Struct.update = mock_update
        try:
            result = dict_to_struct(data)
            assert isinstance(result, struct_pb2.Struct)
            # Should return empty struct on failure
        finally:
            struct_pb2.Struct.update = original_update


class TestStructToDict:
    """Test protobuf Struct to dictionary conversion."""

    def test_struct_to_dict_valid_struct(self) -> None:
        """Test conversion of valid protobuf Struct."""
        struct = struct_pb2.Struct()
        struct.update({"string_field": "value", "number_field": 42, "bool_field": True})
        result = struct_to_dict(struct)
        assert isinstance(result, dict)
        assert result["string_field"] == "value"
        assert result["number_field"] == 42
        assert result["bool_field"] is True

    def test_struct_to_dict_none_struct(self) -> None:
        """Test conversion with None struct."""
        result = struct_to_dict(None)
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_struct_to_dict_empty_struct(self) -> None:
        """Test conversion of empty struct."""
        struct = struct_pb2.Struct()
        result = struct_to_dict(struct)
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_struct_to_dict_nested_struct(self) -> None:
        """Test conversion of nested struct."""
        struct = struct_pb2.Struct()
        nested_data = {"outer": {"inner": "value"}, "top": "test"}
        struct.update(nested_data)
        result = struct_to_dict(struct)
        assert isinstance(result, dict)
        assert "outer" in result
        assert "top" in result

    def test_struct_to_dict_conversion_failure(self) -> None:
        """Test handling of conversion failures."""
        # Create an invalid struct-like object
        class InvalidStruct:
            pass
        invalid_struct = InvalidStruct()
        result = struct_to_dict(invalid_struct)
        assert isinstance(result, dict)
        assert len(result) == 0


class TestSafeStringFromProtobuf:
    """Test safe string extraction from protobuf fields."""

    def test_safe_string_with_string(self) -> None:
        """Test extraction from string value."""
        value = "test string"
        result = safe_string_from_protobuf(value)
        assert result == "test string"

    def test_safe_string_with_bytes(self) -> None:
        """Test extraction from bytes value."""
        value = b"test bytes"
        result = safe_string_from_protobuf(value)
        assert result == "test bytes"

    def test_safe_string_with_invalid_bytes(self) -> None:
        """Test extraction from invalid UTF-8 bytes."""
        value = b"\xff\xfe\xfd"  # Invalid UTF-8
        result = safe_string_from_protobuf(value)
        assert isinstance(result, str)
        # Should return string representation of bytes

    def test_safe_string_with_none(self) -> None:
        """Test extraction from None value."""
        result = safe_string_from_protobuf(None)
        assert result == ""

    def test_safe_string_with_protobuf_string_value(self) -> None:
        """Test extraction from protobuf with string_value attribute."""
        class MockProtobufValue:
            def __init__(self, value: str) -> None:
                self.string_value = value
        mock_value = MockProtobufValue("protobuf string")
        result = safe_string_from_protobuf(mock_value)
        assert result == "protobuf string"

    def test_safe_string_with_no_string_value_attribute(self) -> None:
        """Test extraction from object without string_value attribute."""
        class MockObject:
            def __str__(self) -> str:
                return "mock object string"
        mock_obj = MockObject()
        result = safe_string_from_protobuf(mock_obj)
        assert result == "mock object string"

    def test_safe_string_with_number(self) -> None:
        """Test extraction from number value."""
        value = 42
        result = safe_string_from_protobuf(value)
        assert result == "42"

    def test_safe_string_with_boolean(self) -> None:
        """Test extraction from boolean value."""
        value = True
        result = safe_string_from_protobuf(value)
        assert result == "True"

    def test_safe_string_with_exception_in_str(self) -> None:
        """Test extraction when str() raises exception."""
        class ProblematicObject:
            def __str__(self) -> str:
                msg = "Cannot convert to string"
                raise ValueError(msg)
        obj = ProblematicObject()
        result = safe_string_from_protobuf(obj)
        assert result == ""


class TestConvertersIntegration:
    """Test integration scenarios between converter functions."""

    def test_dict_struct_roundtrip(self) -> None:
        """Test converting dict to struct and back to dict."""
        original_data = {
            "string": "value",
            "number": 42,
            "boolean": True,
            "nested": {"inner": "value"},
        }
        # Convert to struct and back
        struct = dict_to_struct(original_data)
        result_data = struct_to_dict(struct)
        assert isinstance(result_data, dict)
        assert "string" in result_data
        assert "number" in result_data
        assert "boolean" in result_data

    def test_datetime_conversion_chain(self) -> None:
        """Test datetime conversion in complex data structures."""
        dt = datetime(2025, 1, 20, 12, 0, 0, tzinfo=UTC)
        data = {"created_at": dt, "metadata": {"updated_at": dt, "name": "test"}}
        struct = dict_to_struct(data)
        result = struct_to_dict(struct)
        assert isinstance(result, dict)
        assert "created_at" in result
        assert "metadata" in result

    def test_protobuf_timestamp_extraction(self) -> None:
        """Test extracting string from protobuf timestamp."""
        dt = datetime(2025, 1, 20, 12, 0, 0, tzinfo=UTC)
        timestamp = datetime_to_timestamp(dt)
        result = safe_string_from_protobuf(timestamp)
        assert isinstance(result, str)
        assert len(result) > 0
