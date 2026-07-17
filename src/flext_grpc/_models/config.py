"""Flext-grpc config models (pure Pydantic; no project/flext imports).

Typed, frozen shapes for the ``config/*.yaml`` business-rule SSOT. This module
imports **nothing** but ``pydantic`` — the ``_config.py`` facade validates the
model-less YAML slices into these classes and exposes the ready objects under
``config.Grpc.<domain>``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FlextGrpcConfigModels:
    """Namespace of typed flext-grpc config models (pure Pydantic)."""

    class Network(BaseModel):
        """gRPC network defaults and validation thresholds."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default_channel_ready_timeout: float = Field(
            ge=0, description="Seconds to wait for a channel to become ready."
        )
        default_graceful_shutdown_timeout: float = Field(
            ge=0, description="Seconds to wait during graceful shutdown."
        )
        default_host: str = Field(description="Default bind/connect host.")
        default_keepalive_time_ms: int = Field(
            ge=0, description="Keepalive probe interval in milliseconds."
        )
        default_keepalive_timeout_ms: int = Field(
            ge=0, description="Keepalive probe timeout in milliseconds."
        )
        default_port: int = Field(
            ge=1, le=65535, description="Default gRPC port."
        )
        default_timeout: float = Field(
            ge=0, description="Default request timeout in seconds."
        )
        host_pattern: str = Field(description="Regex validating a host name.")
        max_port: int = Field(ge=1, le=65535, description="Maximum valid port.")
        min_port: int = Field(ge=1, le=65535, description="Minimum valid port.")

    class Performance(BaseModel):
        """gRPC message and thread-pool performance limits."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default_message_length: int = Field(
            ge=1, description="Default maximum message length in bytes."
        )
        default_thread_pool_size: int = Field(
            ge=1, description="Default executor thread-pool size."
        )
        max_message_length: int = Field(
            ge=1, description="Absolute maximum message length in bytes."
        )
        max_thread_pool_size: int = Field(
            ge=1, description="Absolute maximum thread-pool size."
        )
        min_message_length: int = Field(
            ge=1, description="Absolute minimum message length in bytes."
        )
        min_thread_pool_size: int = Field(
            ge=1, description="Absolute minimum thread-pool size."
        )

    class Service(BaseModel):
        """gRPC server/worker policy defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default_max_concurrent_rpcs: int = Field(
            ge=1, description="Default RPC concurrency limit."
        )
        default_max_workers: int = Field(
            ge=1, description="Default worker pool size."
        )
        max_workers: int = Field(ge=1, description="Maximum worker pool size.")
        min_workers: int = Field(ge=1, description="Minimum worker pool size.")

    class Streaming(BaseModel):
        """gRPC streaming buffer and concurrency policy."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        bidirectional_queue_size: int = Field(
            ge=1, description="Bidirectional stream queue size."
        )
        client_buffer_threshold: int = Field(
            ge=1, description="Client-stream buffer threshold."
        )
        default_buffer_size: int = Field(
            ge=1, description="Default per-stream buffer size."
        )
        default_max_concurrent_streams: int = Field(
            ge=1, description="Default concurrent stream limit."
        )
        max_buffer_size: int = Field(
            ge=1, description="Absolute maximum buffer size."
        )
        min_buffer_size: int = Field(
            ge=1, description="Absolute minimum buffer size."
        )
        server_batch_size: int = Field(
            ge=1, description="Server-stream batch size."
        )

    class ConnectionPool(BaseModel):
        """gRPC connection-pool defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default_pool_size: int = Field(
            ge=1, description="Default number of pooled channels."
        )

    class Grpc(BaseModel):
        """Root gRPC business-rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        network: FlextGrpcConfigModels.Network = Field(
            description="Network defaults and validation thresholds."
        )
        performance: FlextGrpcConfigModels.Performance = Field(
            description="Message and thread-pool performance limits."
        )
        service: FlextGrpcConfigModels.Service = Field(
            description="Server/worker policy defaults."
        )
        streaming: FlextGrpcConfigModels.Streaming = Field(
            description="Streaming buffer and concurrency policy."
        )
        connection_pool: FlextGrpcConfigModels.ConnectionPool = Field(
            description="Connection-pool defaults."
        )

    class Root(BaseModel):
        """Root flext-grpc runtime config validated from ``config/*.yaml``."""

        model_config = ConfigDict(frozen=True, extra="ignore")

        Grpc: FlextGrpcConfigModels.Grpc = Field(
            description="gRPC business-rule config namespace."
        )


__all__: list[str] = ["FlextGrpcConfigModels"]
