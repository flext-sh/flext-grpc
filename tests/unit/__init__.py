# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("TestsFlextGrpcApi",),
        ".test_config": ("TestsFlextGrpcConfig",),
        ".test_constants": ("TestsFlextGrpcConstantsUnit",),
        ".test_entities": ("TestsFlextGrpcEntities",),
        ".test_errors": ("TestsFlextGrpcErrors",),
        ".test_models": ("TestsFlextGrpcModelsUnit",),
        ".test_protocols": ("TestsFlextGrpcProtocolsUnit",),
        ".test_services": ("TestsFlextGrpcServices",),
        ".test_typings": ("TestsFlextGrpcTypesUnit",),
        ".test_utilities": ("TestsFlextGrpcUtilitiesUnit",),
        "flext_tests": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
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
