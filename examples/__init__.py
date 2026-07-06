# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from examples.typings import (
        ExamplesFlextGrpcTypes as ExamplesFlextGrpcTypes,
        t as t,
    )
    from flext_core._root_typing_parts.facades import (
        c as c,
        d as d,
        e as e,
        h as h,
        m as m,
        p as p,
        r as r,
        s as s,
        u as u,
        x as x,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".typings": (
            "ExamplesFlextGrpcTypes",
            "t",
        ),
        "flext_core._root_typing_parts.facades": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
