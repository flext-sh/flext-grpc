"""Protocol Buffer utility functions for converting between data types.

Consolidates ALL protobuf conversion logic to eliminate duplication
across server.py and handlers.py files.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from google.protobuf import struct_pb2, timestamp_pb2
from google.protobuf.json_format import MessageToDict


def datetime_to_timestamp(dt: datetime | str | None) -> timestamp_pb2.Timestamp:
    """Convert datetime to protobuf Timestamp.

    Provides centralized datetime conversion logic for all server components.

    Args:
        dt: Datetime object, ISO string, or None to convert

    Returns:
        Protobuf Timestamp object

    """
    timestamp = timestamp_pb2.Timestamp()
    if dt is not None:
        if isinstance(dt, str):
            # Parse ISO format string back to datetime
            dt = datetime.fromisoformat(dt)
        timestamp.FromDatetime(dt)
    return timestamp


def dict_to_struct(data: dict[str, Any]) -> struct_pb2.Struct:
    """Convert Python dict to protobuf Struct.

    Args:
        data: Python dictionary to convert

    Returns:
        Protobuf Struct object

    """
    import json
    from datetime import datetime

    struct = struct_pb2.Struct()

    # Handle None data gracefully
    if data is None:
        return struct

    def serialize_value(value: Any) -> Any:
        """Serialize value to be compatible with protobuf Struct."""
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: serialize_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [serialize_value(item) for item in value]
        # Check if value is JSON serializable (covers str, int, float, bool, None)
        try:
            json.dumps(value)
            return value
        except (TypeError, ValueError):
            # If not JSON serializable, convert to string
            return str(value)

    try:
        serialized_data = serialize_value(data)
        struct.update(serialized_data)
    except (ValueError, TypeError):
        # Fallback to empty struct if conversion fails
        pass
    return struct


def struct_to_dict(struct: struct_pb2.Struct | None) -> dict[str, Any]:
    """Convert protobuf Struct to Python dict.

    Handles None values gracefully and provides consistent conversion logic.

    Args:
        struct: Protobuf Struct to convert (can be None)

    Returns:
        Python dictionary representation

    """
    if not struct:
        return {}
    try:
        return MessageToDict(struct)
    except (AttributeError, ValueError, TypeError, Exception):
        return {}


def safe_string_from_protobuf(value: Any) -> str:
    """Safely extract string value from protobuf field.

    Provides robust string extraction logic for protobuf fields.

    Args:
        value: Protobuf value to extract string from

    Returns:
        String representation of the value

    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return str(value)

    # Check for protobuf string_value attribute (common in protobuf Value objects)
    if hasattr(value, "string_value"):
        try:
            return str(value.string_value)
        except (ValueError, TypeError, Exception):
            return ""

    try:
        return str(value)
    except (ValueError, TypeError, Exception):
        return ""
