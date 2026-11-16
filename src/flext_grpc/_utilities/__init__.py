# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._utilities.base import FlextGrpcUtilitiesBase
    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc
    from flext_grpc._utilities.grpc_runtime import FlextGrpcUtilitiesGrpcRuntime
    from flext_grpc._utilities.grpc_service import FlextGrpcUtilitiesGrpcService
    from flext_grpc._utilities.schema_codegen import FlextGrpcUtilitiesSchemaCodegen


__all__: tuple[str, ...] = (
    "FlextGrpcUtilitiesBase",
    "FlextGrpcUtilitiesGrpc",
    "FlextGrpcUtilitiesGrpcRuntime",
    "FlextGrpcUtilitiesGrpcService",
    "FlextGrpcUtilitiesSchemaCodegen",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextGrpcUtilitiesBase": ".base",
        "FlextGrpcUtilitiesGrpc": ".grpc",
        "FlextGrpcUtilitiesGrpcRuntime": ".grpc_runtime",
        "FlextGrpcUtilitiesGrpcService": ".grpc_service",
        "FlextGrpcUtilitiesSchemaCodegen": ".schema_codegen",
    },
    public_exports=__all__,
    deferred_members={
        "FlextGrpcUtilitiesGrpc": (
            "create_channel_entity",
            "create_client_entity",
            "create_server_entity",
            "create_service_entity",
            "create_stream_entity",
            "parse_address",
            "parse_target",
            "validate_target",
            "validate_port",
            "validate_host",
            "format_address",
            "channel_state_name",
            "server_state_name",
            "system_info",
        ),
        "FlextGrpcUtilitiesGrpcRuntime": (
            "_logger",
            "_GrpcRuntimeAdapter",
            "resolve_runtime",
            "runtime_error_message",
            "runtime_failure_message",
            "_runtime_exception_types",
            "call_runtime",
            "run_runtime",
            "open_insecure_channel",
            "create_runtime_server",
            "bind_insecure_port",
        ),
        "FlextGrpcUtilitiesGrpcService": (
            "_HandlerServicer",
            "method_descriptor",
            "encode_message",
            "decode_message",
            "invoke_unary",
            "register_service",
        ),
        "FlextGrpcUtilitiesSchemaCodegen": (
            "_SNAKE_PARTS",
            "_DESCRIPTOR_CHUNK_WIDTH",
            "_RELEASE_PART_COUNT",
            "_CHANNEL_CALLS",
            "_CALLABLE_NAMES",
            "_HANDLER_FACTORIES",
            "generate",
            "python_method_name",
            "_schema_sources",
            "_compile",
            "_plan",
            "_emit_pb2",
            "_emit_pb2_grpc",
            "_methods",
            "_message_name",
            "_version_guard",
            "_stub_class",
            "_servicer_class",
            "_registration",
            "_all_assignment",
            "_descriptor_assignment",
            "_declared_floor",
            "_projection_path",
            "_module_name",
        ),
    },
)
