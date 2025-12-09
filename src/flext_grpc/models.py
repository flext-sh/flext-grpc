"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

from flext_core import m as m_core
from flext_core.utilities import u as flext_u
from pydantic import Field


class FlextGrpcModels(m_core):
    """gRPC domain models extending flext-core FlextModels.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextGrpcModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        flext_u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextGrpcModels is deprecated. Use FlextModels directly with composition instead.",
        )

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Domain:
        """Domain models for gRPC core business entities."""

        class StreamInfo(m_core.Value):
            """Basic stream information (immutable value object)."""

            stream_id: str
            stream_type: str
            target: str
            created_at: datetime = Field(default_factory=datetime.now)
            total_requests_sent: int = Field(default=0)
            average_latency_ms: float = Field(default=0.0)
            error_count: int = Field(default=0)

        class GrpcRequest(m_core.Value):
            """Basic gRPC request model (immutable value object)."""

            method: str = Field(description="gRPC method name")
            data: dict[str, object] | None = Field(
                default=None,
                description="Request data",
            )
            metadata: dict[str, object] | None = Field(
                default=None,
                description="Request metadata",
            )

        class GrpcHealthCheck(m_core.Value):
            """gRPC health check model (immutable value object)."""

            service_name: str = Field(description="Service name")
            status: str = Field(description="Health status")
            timestamp: datetime = Field(description="Check timestamp")

        class ServiceDefinition(m_core.Value):
            """gRPC service definition model (immutable value object)."""

            service_name: str = Field(description="Service name")
            methods: list[str] = Field(
                default_factory=list,
                description="Service methods",
            )
            endpoint: str | None = Field(default=None, description="Service endpoint")
            metadata: dict[str, object] | None = Field(
                default=None,
                description="Service metadata",
            )

        class StreamMetrics(m_core.Value):
            """gRPC stream metrics model (immutable value object)."""

            stream_id: str = Field(description="Stream ID")
            throughput_rps: float = Field(
                description="Throughput in requests per second",
            )
            latency_p50: float = Field(description="50th percentile latency")
            latency_p95: float = Field(description="95th percentile latency")
            latency_p99: float = Field(description="99th percentile latency")
            error_rate: float = Field(description="Error rate")
            memory_usage_bytes: int = Field(description="Memory usage in bytes")

        class ServiceMetrics(m_core.Value):
            """gRPC service metrics model (immutable value object)."""

            service_name: str = Field(description="Service name")
            total_requests: int = Field(description="Total requests")
            successful_requests: int = Field(description="Successful requests")
            failed_requests: int = Field(description="Failed requests")
            avg_response_time: float = Field(description="Average response time")
            active_connections: int = Field(description="Active connections")

    # =========================================================================
    # CONFIGURATION MODELS - Configuration-related models
    # =========================================================================

    class GrpcConfig:
        """Configuration models for gRPC settings."""

        class ServerConfig(m_core.Value):
            """Basic server configuration (immutable value object)."""

            host: str = Field(default="localhost")
            port: int = Field(default=50051)
            max_workers: int = Field(default=10)
            timeout: float = Field(default=30.0)

        class ClientConfig(m_core.Value):
            """Basic client configuration (immutable value object)."""

            target: str = Field(default="localhost:50051")
            timeout: float = Field(default=30.0)

        class ChannelConfig(m_core.Value):
            """Basic channel configuration (immutable value object)."""

            address: str
            options: dict[str, object] | None = None


# =============================================================================
# POPULATE FlextModels.Grpc NAMESPACE
# =============================================================================
# Copy all models from FlextGrpcModels to FlextModels.Grpc namespace
# This allows access via both:
# - FlextGrpcModels.* (backward compatibility, deprecated)
# - FlextModels.Grpc.* (new namespace pattern)
# - m.Grpc.* (convenience alias)
# =============================================================================

# Get all attributes from FlextGrpcModels that are models, classes, or type aliases
# Exclude private attributes and special methods
_grpc_model_attrs = {
    name: attr
    for name, attr in vars(FlextGrpcModels).items()
    if not name.startswith("_")
    and (
        isinstance(attr, type)
        or hasattr(attr, "__origin__")  # TypeAlias
        or (callable(attr) and not isinstance(attr, type(FlextGrpcModels.__init__)))
    )
}

# Note: FlextModels.Grpc namespace does not exist in flext-core
# Models should be accessed directly via FlextGrpcModels.*

m = FlextGrpcModels
m_grpc = FlextGrpcModels

__all__ = ["FlextGrpcModels", "m", "m_grpc"]
