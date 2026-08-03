"""FLEXT gRPC settings — namespaced under ``settings.Grpc``.

Universal fields via MRO; project fields in the ``Grpc`` group with simple
scalar types (env-settable). Advanced per-domain gRPC configuration objects are
built by consumers from these scalars, not stored as complex settings fields.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings, m


class FlextGrpcSettings(FlextSettings):
    """gRPC runtime settings; fields under ``settings.Grpc.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_GRPC_", env_nested_delimiter="__", extra="ignore"
    )

    class _Grpc(m.BaseModel):
        """Namespaced gRPC runtime settings."""

        host: Annotated[str, m.Field(default="127.0.0.1", description="gRPC bind host")]
        port: Annotated[
            int, m.Field(default=50051, ge=1, le=65535, description="gRPC bind port")
        ]
        max_workers: Annotated[
            int, m.Field(default=100, ge=1, description="Max worker threads")
        ]
        timeout: Annotated[
            float, m.Field(default=30.0, gt=0, description="Request timeout (s)")
        ]

    if TYPE_CHECKING:
        Grpc: _Grpc
    else:
        Grpc: _Grpc = m.Field(
            default_factory=_Grpc, description="Namespaced gRPC settings."
        )


settings: FlextGrpcSettings = FlextGrpcSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_grpc import settings``."""

__all__: list[str] = ["FlextGrpcSettings", "settings"]
