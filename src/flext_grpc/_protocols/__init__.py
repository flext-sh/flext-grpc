# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._protocols.base import FlextGrpcProtocolsBase
    from flext_grpc._protocols.channel_protocols import FlextGrpcProtocolsChannel
    from flext_grpc._protocols.config import FlextGrpcProtocolsConfig
    from flext_grpc._protocols.connection_protocols import FlextGrpcProtocolsConnection
    from flext_grpc._protocols.resource_protocols import FlextGrpcProtocolsResource
    from flext_grpc._protocols.server_protocols import FlextGrpcProtocolsServer
    from flext_grpc._protocols.service_protocols import FlextGrpcProtocolsService
    from flext_grpc._protocols.stream_protocols import FlextGrpcProtocolsStream


__all__: tuple[str, ...] = (
    "FlextGrpcProtocolsBase",
    "FlextGrpcProtocolsChannel",
    "FlextGrpcProtocolsConfig",
    "FlextGrpcProtocolsConnection",
    "FlextGrpcProtocolsResource",
    "FlextGrpcProtocolsServer",
    "FlextGrpcProtocolsService",
    "FlextGrpcProtocolsStream",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcProtocolsBase": ".base",
        "FlextGrpcProtocolsChannel": ".channel_protocols",
        "FlextGrpcProtocolsConfig": ".config",
        "FlextGrpcProtocolsConnection": ".connection_protocols",
        "FlextGrpcProtocolsResource": ".resource_protocols",
        "FlextGrpcProtocolsServer": ".server_protocols",
        "FlextGrpcProtocolsService": ".service_protocols",
        "FlextGrpcProtocolsStream": ".stream_protocols",
    }),
    public_exports=__all__,
)
