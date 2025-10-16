"""Project wrapper for shared FLEXT gRPC documentation synchronization tooling."""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
os.environ.setdefault("FLEXT_DOC_PROJECT_ROOT", _PROJECT_ROOT)
os.environ.setdefault("FLEXT_DOC_PROFILE", "grpc")

from flext_quality.docs_maintenance.profiles.grpc.sync import *


def _run_cli() -> None:
    """Invoke the shared CLI entry point."""
    from flext_quality.docs_maintenance.profiles.grpc.sync import main

    main()


if __name__ == "__main__":
    _run_cli()
