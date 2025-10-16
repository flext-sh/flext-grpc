"""Project wrapper for shared FLEXT gRPC documentation reporting."""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
os.environ.setdefault("FLEXT_DOC_PROJECT_ROOT", _PROJECT_ROOT)
os.environ.setdefault("FLEXT_DOC_PROFILE", "grpc")

from flext_quality.docs_maintenance.profiles.grpc.reporting import *


def _run_cli() -> None:
    """Invoke the shared CLI entry point."""
    from flext_quality.docs_maintenance.profiles.grpc.reporting import main

    main()


if __name__ == "__main__":
    _run_cli()
