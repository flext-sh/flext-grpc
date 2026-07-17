"""FlextGrpcConfig — frozen, validated config singleton for flext-grpc (ADR-005 §7).

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call (model-less, ``extra=allow`` at the FlextConfig base). The
flat YAML is then validated into the pure-Pydantic ``_models.config`` shapes and
exposed as typed domain objects under ``config.Grpc.<domain>`` — never a
model-less dict subscript.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import ClassVar

from flext_core import FlextConfig
from flext_grpc._models.config import FlextGrpcConfigModels

# NOTE (multi-agent): accessor typed by PROTOCOL (p), never the model
# class; the protocol module enters under TYPE_CHECKING only (§2.5/§3.4).
from flext_grpc._protocols.config import FlextGrpcProtocolsConfig


class FlextGrpcConfig(FlextConfig):
    """Grpc config auto-loaded from ``config/*.yaml`` and validated via models."""

    # NOTE (multi-agent): anchored to the project root so the YAML SSOT loads
    # regardless of the caller's CWD (library code must not depend on CWD).
    CONFIG_DIR: ClassVar[str] = str(Path(__file__).resolve().parents[2] / "config")

    @cached_property
    def Grpc(self) -> FlextGrpcProtocolsConfig.Grpc:
        """Validated ``Grpc`` business-rule config namespace."""
        root = FlextGrpcConfigModels.Root.model_validate(
            dict(self.model_extra or {}),
        )
        return root.Grpc


config: FlextGrpcConfig = FlextGrpcConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_grpc import config``."""

__all__: list[str] = ["FlextGrpcConfig", "config"]
