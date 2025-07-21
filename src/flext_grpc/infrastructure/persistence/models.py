"""SQLAlchemy models for FLEXT-GRPC.

Using flext-core patterns - NO duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as POSTGRESQL_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


class GRPCServiceModel(Base):
    """SQLAlchemy model for gRPC services."""

    __tablename__ = "grpc_services"

    # Primary key
    id: Mapped[UUID] = mapped_column(POSTGRESQL_UUID(as_uuid=True), primary_key=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)

    # Configuration
    max_workers: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    max_concurrent_rpcs: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
    )
    max_message_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=104857600,
    )

    # TLS configuration
    ssl_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ssl_cert_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ssl_key_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ssl_ca_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Health tracking
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_health_check: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    error_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    # Relationships
    methods: Mapped[list[RPCMethodModel]] = relationship(
        "RPCMethodModel",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert the gRPC service model to a dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the service model.

        """
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "host": self.host,
            "port": self.port,
            "max_workers": self.max_workers,
            "max_concurrent_rpcs": self.max_concurrent_rpcs,
            "max_message_size": self.max_message_size,
            "ssl_enabled": self.ssl_enabled,
            "ssl_cert_path": self.ssl_cert_path,
            "ssl_key_path": self.ssl_key_path,
            "ssl_ca_path": self.ssl_ca_path,
            "started_at": self.started_at,
            "last_health_check": self.last_health_check,
            "error_count": self.error_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class RPCMethodModel(Base):
    """SQLAlchemy model for RPC methods."""

    __tablename__ = "rpc_methods"

    # Primary key
    id: Mapped[UUID] = mapped_column(POSTGRESQL_UUID(as_uuid=True), primary_key=True)

    # Foreign key
    service_id: Mapped[UUID] = mapped_column(
        POSTGRESQL_UUID(as_uuid=True),
        ForeignKey("grpc_services.id"),
        nullable=False,
    )

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    method_type: Mapped[str] = mapped_column(String(50), nullable=False)
    request_type: Mapped[str] = mapped_column(String(255), nullable=False)
    response_type: Mapped[str] = mapped_column(String(255), nullable=False)

    # Configuration
    timeout_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=30.0)
    retry_policy: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default={},
    )

    # Metrics
    call_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_response_time_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    # Relationships
    service: Mapped[GRPCServiceModel] = relationship(
        "GRPCServiceModel",
        back_populates="methods",
    )
    calls: Mapped[list[RPCCallModel]] = relationship(
        "RPCCallModel",
        back_populates="method",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert the RPC method model to a dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the method model.

        """
        return {
            "id": self.id,
            "service_id": self.service_id,
            "name": self.name,
            "method_type": self.method_type,
            "request_type": self.request_type,
            "response_type": self.response_type,
            "timeout_seconds": self.timeout_seconds,
            "retry_policy": self.retry_policy,
            "call_count": self.call_count,
            "error_count": self.error_count,
            "avg_response_time_ms": self.avg_response_time_ms,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class RPCCallModel(Base):
    """SQLAlchemy model for RPC calls."""

    __tablename__ = "rpc_calls"

    # Primary key
    id: Mapped[UUID] = mapped_column(POSTGRESQL_UUID(as_uuid=True), primary_key=True)

    # Foreign key
    method_id: Mapped[UUID] = mapped_column(
        POSTGRESQL_UUID(as_uuid=True),
        ForeignKey("rpc_methods.id"),
        nullable=False,
    )

    # Call details
    client_id: Mapped[str] = mapped_column(String(255), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Metadata
    request_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    response_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    call_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default={},
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    # Relationships
    method: Mapped[RPCMethodModel] = relationship(
        "RPCMethodModel",
        back_populates="calls",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert the RPC call model to a dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the call model.

        """
        return {
            "id": self.id,
            "method_id": self.method_id,
            "client_id": self.client_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "error_message": self.error_message,
            "request_size_bytes": self.request_size_bytes,
            "response_size_bytes": self.response_size_bytes,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
