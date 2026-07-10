"""FlextGrpcConfig — frozen config singleton for flext-grpc (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Grpc:`` key and
are exposed through the open ``config.Grpc`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Grpc.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_cli import FlextCliConfig


class _GrpcNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextGrpcConfig(FlextCliConfig):
    """Grpc config auto-loaded model-less from ``config/*.yaml``."""

    Grpc: _GrpcNamespace = _GrpcNamespace()


config: FlextGrpcConfig = FlextGrpcConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_grpc import config``."""

__all__: list[str] = ["FlextGrpcConfig", "config"]
