"""FLEXT gRPC settings — namespaced under ``settings.Grpc``.

Universal fields via MRO; project fields in the ``Grpc`` group with simple
scalar types (env-settable). Advanced per-domain gRPC configuration objects are
built by consumers from these scalars, not stored as complex settings fields.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextSettings, m


class FlextGrpcSettings(FlextSettings):
    """gRPC runtime settings; fields under ``settings.Grpc.*``."""

    model_config = m.SettingsConfigDict(
        env_prefix="FLEXT_GRPC_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class GrpcSettings(m.BaseModel):
        """Namespaced gRPC runtime settings.

        Defaults live on the assignment side (checker-visible optional
        constructor parameters).
        """

        host: Annotated[str, m.Field(description="gRPC bind host")] = "127.0.0.1"
        port: Annotated[
            int,
            m.Field(ge=1, le=65535, description="gRPC bind port"),
        ] = 50051
        max_workers: Annotated[
            int,
            m.Field(ge=1, description="Max worker threads"),
        ] = 100
        timeout: Annotated[
            float,
            m.Field(gt=0, description="Request timeout (s)"),
        ] = 30.0

    Grpc: GrpcSettings = m.Field(
        default_factory=GrpcSettings,
        description="Namespaced gRPC settings.",
    )


settings: FlextGrpcSettings = FlextGrpcSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_grpc import settings``."""

__all__: list[str] = ["FlextGrpcSettings", "settings"]
