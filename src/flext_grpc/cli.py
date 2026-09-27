"""CLI facade for flext-grpc — thin transport adapter.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli.services.cli import FlextCliCli

if TYPE_CHECKING:
    from flext_core import t


class FlextGrpcCli(FlextCliCli):
    """Flext-grpc CLI facade — extends flext-cli CLI."""


def main(args: t.StrSequence | None = None) -> int:
    """Console-script entry point — commands are not implemented yet."""
    _ = args
    return 0


__all__: t.VariadicTuple[str] = ("FlextGrpcCli", "main")
