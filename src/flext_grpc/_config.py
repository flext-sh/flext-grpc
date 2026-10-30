"""FlextGrpcConfig — frozen config singleton for flext-grpc (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Grpc:`` key and
are exposed through the open ``config.Grpc`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Grpc.<domain>[<key>...]``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextConfig
from pydantic import Field

from flext_grpc.config_models import FlextGrpcModelsConfigNamespace


class FlextGrpcConfig(FlextConfig):
    """Grpc config auto-loaded model-less from ``config/*.yaml``."""

    Grpc: Annotated[
        FlextGrpcModelsConfigNamespace.GrpcNamespace,
        Field(
            description="Open namespace exposing ``config/*.yaml`` under ``Grpc``.",
        ),
    ] = FlextGrpcModelsConfigNamespace.GrpcNamespace()


config: FlextGrpcConfig = FlextGrpcConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_grpc import config``."""

__all__: list[str] = ["FlextGrpcConfig", "config"]
