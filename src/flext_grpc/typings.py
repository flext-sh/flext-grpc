"""FLEXT gRPC Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping
from typing import Literal

from flext_cli import t


class FlextGrpcTypes(t):
    """gRPC-specific type definitions extending t via MRO."""

    class Grpc:
        """gRPC domain namespace (flat members per AGENTS.md §149)."""

        type EntityKind = Literal["server", "client", "channel", "service", "stream"]
        type Headers = t.StrMapping
        type ConfigDict = Mapping[str, t.Scalar | t.JsonValue | None]

        @staticmethod
        def parse_target(target: str) -> tuple[str, int]:
            """Parse a validated gRPC target into (host, port)."""
            if not FlextGrpcTypes.Grpc.validate_target(target):
                msg = f"Invalid gRPC target: {target}"
                raise ValueError(msg)
            host, port_str = target.split(":", 1)
            return (host, int(port_str))

        @staticmethod
        def validate_target(target: str) -> bool:
            """Validate a gRPC target string in the form host:port."""
            if not target or ":" not in target:
                return False
            try:
                host, port_str = target.split(":", 1)
                if not host or not port_str:
                    return False
                if not re.match(r"^[a-zA-Z0-9.-]+$", host):
                    return False
                port = int(port_str)
                max_port = 65535
                return 1 <= port <= max_port
            except (ValueError, AttributeError):
                logger = logging.getLogger(__name__)
                logger.debug("Invalid gRPC target: %s", target)
                return False


t = FlextGrpcTypes
__all__: list[str] = ["FlextGrpcTypes", "t"]
