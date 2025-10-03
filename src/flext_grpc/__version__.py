"""Version metadata for flext grpc using importlib.metadata."""

from __future__ import annotations

from importlib.metadata import metadata

_metadata = metadata("flext-grpc")

__version__ = _metadata["Version"]
__version_info__ = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)

__all__ = ["__version__", "__version_info__"]
