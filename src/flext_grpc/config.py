"""FLEXT gRPC Configuration - Simplified config using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextBaseSettings
from pydantic import Field, field_validator

from flext_grpc.constants import FLEXT_GRPC_MAX_PORT, FLEXT_GRPC_MIN_PORT
from flext_grpc.errors import FlextGrpcConfigurationError

class FlextGrpcConfig(FlextBaseSettings):
    """Simplified gRPC configuration."""

    host: str = Field(default="localhost")
    port: int = Field(default=50051)
    max_workers: int = Field(default=10)
    timeout: float = Field(default=30.0)

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        if not v or not v.strip():
            raise FlextGrpcConfigurationError("Host cannot be empty")
        return v.strip()

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not (FLEXT_GRPC_MIN_PORT <= v <= FLEXT_GRPC_MAX_PORT):
            raise FlextGrpcConfigurationError(
                f"Port {v} must be between {FLEXT_GRPC_MIN_PORT} and {FLEXT_GRPC_MAX_PORT}"
            )
        return v

    @field_validator("max_workers")
    @classmethod
    def validate_max_workers(cls, v: int) -> int:
        if v < 1:
            raise FlextGrpcConfigurationError("Max workers must be >= 1")
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        if v <= 0:
            raise FlextGrpcConfigurationError("Timeout must be positive")
        return v

    def get_address(self) -> str:
        return f"{self.host}:{self.port}"

__all__ = ["FlextGrpcConfig"]
