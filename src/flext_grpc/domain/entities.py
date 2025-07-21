"""Domain entities for FLEXT-GRPC.

REFACTORED:
            Uses flext-core mixins, types, StrEnum, and constants - NO duplication.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from flext_core.domain.constants import ConfigDefaults
from flext_core.domain.pydantic_base import DomainEntity, DomainEvent, Field

if TYPE_CHECKING:
    from flext_core.domain.types import EntityId, Version


class ServiceStatus(StrEnum):
    """gRPC service status using StrEnum for type safety."""

    RUNNING = "running"
    STOPPED = "stopped"
    STARTING = "starting"
    STOPPING = "stopping"
    ERROR = "error"


class RPCMethodType(StrEnum):
    """gRPC method types using StrEnum for type safety."""

    UNARY = "unary"
    SERVER_STREAMING = "server_streaming"
    CLIENT_STREAMING = "client_streaming"
    BIDIRECTIONAL_STREAMING = "bidirectional_streaming"


class GRPCService(DomainEntity):
    """gRPC service domain entity using enhanced mixins for code reduction."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    version: Version = Field(
        "0.7.0",
        description="Service version",
    )
    service_status: ServiceStatus = Field(default=ServiceStatus.STOPPED)
    host: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    port: int = Field(..., ge=1, le=65535)

    # Service configuration
    max_workers: int = Field(
        default=10,
        ge=1,
        le=ConfigDefaults.MAX_PAGE_SIZE,
    )
    max_concurrent_rpcs: int = Field(
        default=ConfigDefaults.MAX_PAGE_SIZE,
        ge=1,
        le=1000,
    )
    max_message_size: int = Field(default=104857600, ge=1024)  # 100MB

    # TLS configuration
    ssl_enabled: bool = Field(default=False)
    ssl_cert_path: str | None = None
    ssl_key_path: str | None = None
    ssl_ca_path: str | None = None

    # Health tracking
    started_at: datetime | None = None
    last_health_check: datetime | None = None
    error_count: int = Field(default=0, ge=0)

    @property
    def is_healthy(self) -> bool:
        """Check if gRPC service is healthy.

        Returns:
            True if service is running and has no errors.

        """
        return self.service_status == ServiceStatus.RUNNING and self.error_count == 0

    @property
    def address(self) -> str:
        """Get full network address for gRPC service.

        Returns:
            Combined host:port address string.

        """
        return f"{self.host}:{self.port}"


class RPCMethod(DomainEntity):
    """gRPC method domain entity using enhanced mixins for code reduction."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    service_id: EntityId = Field(..., description="Associated service ID")
    method_type: RPCMethodType = Field(default=RPCMethodType.UNARY)

    # Request/Response types
    request_type: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    response_type: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )

    # Method configuration
    timeout_seconds: float = Field(
        default=ConfigDefaults.DEFAULT_TIMEOUT,
        ge=0.1,
        le=3600.0,
    )
    retry_policy: dict[str, Any] = Field(default_factory=dict)

    # Metrics
    call_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    avg_response_time_ms: float = Field(default=0.0, ge=0.0)

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage for RPC method.

        Returns:
            Success rate as percentage (0-100).

        """
        if self.call_count == 0:
            return 0.0
        return ((self.call_count - self.error_count) / self.call_count) * 100

    @property
    def is_streaming(self) -> bool:
        """Check if RPC method uses streaming.

        Returns:
            True if method is not unary (uses streaming).

        """
        return self.method_type != RPCMethodType.UNARY


class RPCCall(DomainEntity):
    """gRPC call domain entity using enhanced mixins for code reduction."""

    method_id: EntityId = Field(..., description="Associated method ID")
    client_id: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )

    # Call details
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
    duration_ms: float | None = None

    # Status - inherits from StatusMixin in EntityMixin
    call_status: str = Field(..., min_length=1, max_length=50)
    error_message: str | None = Field(
        None,
        max_length=ConfigDefaults.MAX_ERROR_MESSAGE_LENGTH,
    )

    # Metadata - inherits from MetadataMixin in EntityMixin
    request_size_bytes: int = Field(default=0, ge=0)
    response_size_bytes: int = Field(default=0, ge=0)

    @property
    def is_completed(self) -> bool:
        """Check if RPC call has completed.

        Returns:
            True if call has a completion timestamp.

        """
        return self.completed_at is not None

    @property
    def is_successful(self) -> bool:
        """Check if RPC call completed successfully.

        Returns:
            True if call completed without errors.

        """
        return self.is_completed and self.error_message is None


# Domain Events - Using typed IDs for consistency
class ServiceStartedEvent(DomainEvent):
    """Event raised when gRPC service starts."""

    service_id: EntityId
    service_name: str
    address: str


class ServiceStoppedEvent(DomainEvent):
    """Event raised when gRPC service stops."""

    service_id: EntityId
    service_name: str


class RPCCallCompletedEvent(DomainEvent):
    """Event raised when RPC call completes."""

    call_id: EntityId
    method_name: str
