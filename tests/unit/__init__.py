# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.tests.unit.test_api import TestsFlextGrpcApi as TestsFlextGrpcApi
    from flext_grpc.tests.unit.test_config import (
        TestsFlextGrpcConfig as TestsFlextGrpcConfig,
    )
    from flext_grpc.tests.unit.test_constants import (
        TestsFlextGrpcConstantsUnit as TestsFlextGrpcConstantsUnit,
    )
    from flext_grpc.tests.unit.test_entities import (
        TestsFlextGrpcEntities as TestsFlextGrpcEntities,
    )
    from flext_grpc.tests.unit.test_errors import (
        TestsFlextGrpcErrors as TestsFlextGrpcErrors,
    )
    from flext_grpc.tests.unit.test_models import (
        TestsFlextGrpcModelsUnit as TestsFlextGrpcModelsUnit,
    )
    from flext_grpc.tests.unit.test_protocols import (
        TestsFlextGrpcProtocolsUnit as TestsFlextGrpcProtocolsUnit,
    )
    from flext_grpc.tests.unit.test_services import (
        TestsFlextGrpcServices as TestsFlextGrpcServices,
    )
    from flext_grpc.tests.unit.test_typings import (
        TestsFlextGrpcTypesUnit as TestsFlextGrpcTypesUnit,
    )
    from flext_grpc.tests.unit.test_utilities import (
        TestsFlextGrpcUtilitiesUnit as TestsFlextGrpcUtilitiesUnit,
    )
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
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
