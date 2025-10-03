"""Project metadata for flext grpc."""

from __future__ import annotations

from importlib.metadata import metadata
from typing import Final, NamedTuple

_metadata = metadata("flext-grpc")

__version__ = _metadata["Version"]
__version_info__ = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)


class FlextGrpcVersion(NamedTuple):
    """Structured metadata for the flext grpc distribution."""

    version: str
    version_info: tuple[int | str, ...]

    @classmethod
    def current(cls) -> FlextGrpcVersion:
        """Return canonical metadata loaded from pyproject.toml."""
        return cls(version=__version__, version_info=__version_info__)


VERSION: Final[FlextGrpcVersion] = FlextGrpcVersion.current()

__all__ = ["VERSION", "FlextGrpcVersion", "__version__", "__version_info__"]
