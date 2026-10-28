"""Shared service foundation for flext-grpc components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with `s` from flext-core, avoiding duplication of initialization
across gRPC services.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from abc import ABC
from collections.abc import MutableSequence
from typing import override

from flext_core import FlextService

from flext_grpc import FlextGrpcSettings, m, p, r


class FlextGrpcServiceBase(FlextService[FlextGrpcSettings], ABC):
    """Base class for flext-grpc services with typed configuration access.

    Provides typed settings access and a default execute() surface for
    mixins that do not define their own active command.
    """

    _grpc_config: FlextGrpcSettings = m.PrivateAttr(
        default_factory=lambda: FlextGrpcSettings.model_validate({}),
    )

    @property
    def grpc_config(self) -> FlextGrpcSettings:
        """Runtime gRPC configuration bound to this facade instance."""
        return self._grpc_config

    @override
    def execute(self) -> p.Result[FlextGrpcSettings]:
        """Default service execution surface.

        Returns:
            The resulting ``p.Result[FlextGrpcSettings]``.

        """
        return r[FlextGrpcSettings].ok(self.grpc_config)


s = FlextGrpcServiceBase

__all__: MutableSequence[str] = ["FlextGrpcServiceBase", "s"]
