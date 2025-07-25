"""gRPC converters for FLEXT.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Utility functions for converting between Python types and gRPC protobuf types.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

if TYPE_CHECKING:
    from datetime import datetime


def datetime_to_timestamp(dt: datetime) -> Timestamp:
    """Convert datetime to protobuf Timestamp.

    Args:
        dt: Python datetime object

    Returns:
        Protobuf Timestamp object

    """
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp


def dict_to_struct(data: dict[str, Any]) -> Struct:
    """Convert dictionary to protobuf Struct.

    Args:
        data: Python dictionary

    Returns:
        Protobuf Struct object

    """
    struct = Struct()
    struct.update(data)
    return struct


def struct_to_dict(struct: Struct) -> dict[str, Any]:
    """Convert protobuf Struct to dictionary.

    Args:
        struct: Protobuf Struct object

    Returns:
        Python dictionary

    """
    return dict(struct)


def safe_string_from_protobuf(value: str | None) -> str:
    """Safely extract string from protobuf value.

    Args:
        value: String value from protobuf

    Returns:
        Safe string value

    """
    return value or ""
