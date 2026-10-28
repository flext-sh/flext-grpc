"""Canonical producer of the typed gRPC wire-schema projections.

The producer compiles ``protos/*.proto`` with the installed gRPC toolchain,
plans the message and service surface from the compiled descriptor, and emits
``flext_pb2`` and ``flext_pb2_grpc`` as fully annotated, lint-admitted
modules. Runtime behavior stays native: ``flext_pb2`` keeps the protobuf
serialized-descriptor builder contract, and ``flext_pb2_grpc`` keeps the gRPC
stub, servicer and registration surface with unchanged wire paths. The
emitted Python RPC method names are the snake-case projection of the RPC
names, so the generated surface satisfies the fleet naming rules without
exclusions, suppressions or stubs, while the wire contract is preserved
verbatim. Unsupported schema constructs fail loudly instead of being skipped
silently.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import tempfile
import tomllib
from pathlib import Path
from types import MappingProxyType
from typing import ClassVar

from flext_core import u
from google.protobuf import descriptor_pb2
from grpc_tools import protoc

from flext_grpc import p, r


class FlextGrpcUtilitiesSchemaCodegen:
    """Canonical producer of the typed gRPC wire-schema projections."""

    _SNAKE_PARTS: ClassVar[re.Pattern[str]] = re.compile(
        r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])",
    )
    _DESCRIPTOR_CHUNK_WIDTH: ClassVar[int] = 64
    _RELEASE_PART_COUNT: ClassVar[int] = 3
    _CHANNEL_CALLS: ClassVar[MappingProxyType[tuple[bool, bool], str]] = (
        MappingProxyType({
            (False, False): "unary_unary",
            (False, True): "unary_stream",
            (True, False): "stream_unary",
            (True, True): "stream_stream",
        })
    )
    _CALLABLE_NAMES: ClassVar[MappingProxyType[tuple[bool, bool], str]] = (
        MappingProxyType({
            (False, False): "UnaryUnaryMultiCallable",
            (False, True): "UnaryStreamMultiCallable",
            (True, False): "StreamUnaryMultiCallable",
            (True, True): "StreamStreamMultiCallable",
        })
    )
    _HANDLER_FACTORIES: ClassVar[MappingProxyType[tuple[bool, bool], str]] = (
        MappingProxyType({
            (False, False): "unary_unary_rpc_method_handler",
            (False, True): "unary_stream_rpc_method_handler",
            (True, False): "stream_unary_rpc_method_handler",
            (True, True): "stream_stream_rpc_method_handler",
        })
    )

    @classmethod
    def generate(cls) -> p.Result[tuple[tuple[Path, str], ...]]:
        """Compile the declared wire schema and emit its typed projections.

        Returns:
            The resulting ``(destination, content)`` projection candidates.

        """
        result_type = r[tuple[tuple[Path, str], ...]]
        sources = cls._schema_sources()
        if sources.failure:
            return result_type.from_failure(sources)
        compiled = cls._compile(sources.value)
        if compiled.failure:
            return result_type.from_failure(compiled)
        descriptor = cls._plan(compiled.value)
        if descriptor.failure:
            return result_type.from_failure(descriptor)
        service = descriptor.value.service[0]
        return result_type.ok((
            (
                cls._projection_path("flext_pb2.py"),
                cls._emit_pb2(descriptor.value),
            ),
            (
                cls._projection_path("flext_pb2_grpc.py"),
                cls._emit_pb2_grpc(descriptor.value, service),
            ),
        ))

    @classmethod
    def python_method_name(cls, rpc_name: str) -> str:
        """Project one wire RPC name onto its Python method name.

        Args:
            rpc_name: The RPC name declared in the schema.

        Returns:
            The snake-case Python method name emitted for the RPC.

        Raises:
            ValueError: If the RPC name has no projectable parts.

        """
        parts = cls._SNAKE_PARTS.findall(rpc_name)
        if not parts:
            msg = f"RPC name has no projectable parts: {rpc_name}"
            raise ValueError(msg)
        return "_".join(part.lower() for part in parts)

    @classmethod
    def _schema_sources(cls) -> p.Result[tuple[Path, ...]]:
        """Collect the declared schema sources of the protos package.

        Returns:
            The resulting schema paths, or the first failure.

        """
        result_type = r[tuple[Path, ...]]
        protos_dir = Path(__file__).resolve().parents[1] / "protos"
        sources = tuple(sorted(protos_dir.glob("*.proto")))
        if not sources:
            return result_type.fail(f"No wire schema declared under {protos_dir}")
        return result_type.ok(sources)

    @classmethod
    def _compile(cls, sources: tuple[Path, ...]) -> p.Result[bytes]:
        """Compile the schema sources into one serialized descriptor set.

        Args:
            sources: The schema paths declared under the source root.

        Returns:
            The resulting serialized descriptor set, or the first failure.

        """
        result_type = r[bytes]
        src_root = Path(__file__).resolve().parents[2]
        try:
            relatives = tuple(path.relative_to(src_root) for path in sources)
        except ValueError as error:
            return result_type.fail(f"Schema outside the source root: {error}")
        with tempfile.TemporaryDirectory() as staging:
            descriptor_set = Path(staging) / "descriptor.pb"
            arguments: list[str] = [
                "protoc",
                f"--proto_path={src_root}",
                f"--descriptor_set_out={descriptor_set}",
                *(str(relative) for relative in relatives),
            ]
            try:
                code = protoc.main(arguments)
            except SystemExit as exit_error:  # protoc signals CLI errors via SystemExit
                return result_type.fail(
                    f"protoc aborted with system exit {exit_error.code}",
                )
            if code != 0:
                return result_type.fail(
                    f"protoc failed with exit code {code}",
                )
            return u.try_(descriptor_set.read_bytes, catch=OSError)

    @classmethod
    def _plan(
        cls,
        descriptor_set: bytes,
    ) -> p.Result[descriptor_pb2.FileDescriptorProto]:
        """Plan the emitted surface from the compiled descriptor set.

        Args:
            descriptor_set: The serialized descriptor set compiled by protoc.

        Returns:
            The resulting single file descriptor, or the first failure.

        """
        result_type = r[descriptor_pb2.FileDescriptorProto]
        parsed = descriptor_pb2.FileDescriptorSet.FromString(descriptor_set)
        if len(parsed.file) != 1:
            return result_type.fail(
                f"Expected one file descriptor, got {len(parsed.file)}",
            )
        descriptor = parsed.file[0]
        if descriptor.enum_type or any(
            message.enum_type or message.nested_type
            for message in descriptor.message_type
        ):
            return result_type.fail(
                "Wire schema declares enums or nested messages; the typed "
                "producer does not emit them yet",
            )
        if len(descriptor.service) != 1:
            return result_type.fail(
                f"Expected exactly one service, got {len(descriptor.service)}",
            )
        return result_type.ok(descriptor)

    @classmethod
    def _emit_pb2(cls, descriptor: descriptor_pb2.FileDescriptorProto) -> str:
        """Emit the typed protobuf message projection.

        Args:
            descriptor: The compiled file descriptor.

        Returns:
            The emitted ``flext_pb2`` module content.

        """
        proto_version = cls._declared_floor("protobuf")
        lines = [
            "# Generated by the FLEXT wire-schema compiler. DO NOT EDIT!",
            "# Regenerate with: make gen",
            '"""Typed projection of the FLEXT gRPC wire schema.',
            "",
            "Runtime behavior is native protobuf: the serialized file descriptor",
            "is registered in the default descriptor pool and the message classes",
            "are built into this module by the protobuf builder. The typed",
            "aliases after the builder calls give static analysis the message",
            "classes the builder injects at runtime.",
            "",
            "Copyright (c) 2026 FLEXT Team. All rights reserved.",
            "SPDX-License-Identifier: MIT",
            '"""',
            "",
            "from __future__ import annotations",
            "",
            "from google.protobuf import (",
            "    descriptor_pool as _descriptor_pool,",
            "    message as _message,",
            "    runtime_version as _runtime_version,",
            "    symbol_database as _symbol_database,",
            ")",
            "from google.protobuf.internal import builder as _builder",
            "",
            "_runtime_version.ValidateProtobufRuntimeVersion(",
            "    _runtime_version.Domain.PUBLIC,",
            f"    {proto_version[0]},",
            f"    {proto_version[1]},",
            f"    {proto_version[2]},",
            '    "",',
            f'    "{descriptor.name}",',
            ")",
            "",
            "_sym_db = _symbol_database.Default()",
            "",
        ]
        lines.extend(cls._descriptor_assignment(descriptor.SerializeToString()))
        lines.extend([
            "",
            "_globals = globals()",
            "_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)",
            "_builder.BuildTopDescriptorsAndMessages(",
            "    DESCRIPTOR,",
            f'    "{cls._module_name("flext_pb2.py")}",',
            "    _globals,",
            ")",
        ])
        names = ["DESCRIPTOR"]
        lines.append("")
        for message in descriptor.message_type:
            names.append(message.name)
            lines.append(
                f'{message.name}: type[_message.Message] = _globals["{message.name}"]',
            )
        lines.extend(cls._all_assignment(names))
        return "\n".join(lines) + "\n"

    @classmethod
    def _emit_pb2_grpc(
        cls,
        descriptor: descriptor_pb2.FileDescriptorProto,
        service: descriptor_pb2.ServiceDescriptorProto,
    ) -> str:
        """Emit the typed gRPC stub, servicer and registration surface.

        Args:
            descriptor: The compiled file descriptor.
            service: The single declared service of the descriptor.

        Returns:
            The emitted ``flext_pb2_grpc`` module content.

        """
        service_full_name = f"{descriptor.package}.{service.name}"
        grpc_version = cls._declared_floor("grpcio")
        methods = cls._methods(service)
        lines = [
            "# Generated by the FLEXT wire-schema compiler. DO NOT EDIT!",
            "# Regenerate with: make gen",
            '"""Typed client and server surface for the FLEXT gRPC wire schema.',
            "",
            "The Python RPC method names are the snake-case projection of the",
            "RPC names; every wire path is preserved verbatim, so the emitted",
            "stub, servicer and registration surface keep the native gRPC",
            "contract while passing the fleet naming and annotation rules",
            "without exclusions or suppressions. The experimental generated",
            "convenience class is intentionally not emitted; its",
            "``grpc.experimental`` access cannot satisfy the zero-typing",
            "contract and no consumer exercises it.",
            "",
            "Copyright (c) 2026 FLEXT Team. All rights reserved.",
            "SPDX-License-Identifier: MIT",
            '"""',
            "",
            "from __future__ import annotations",
            "",
            "from types import MappingProxyType",
            "from typing import Final",
            "",
            "import grpc",
            "",
            "from flext_grpc.protos import flext_pb2",
            "",
            (
                f'GRPC_GENERATED_VERSION: Final[str] = "{grpc_version[0]}.'
                f'{grpc_version[1]}.{grpc_version[2]}"'
            ),
            '"""Minimum ``grpcio`` release the surface was compiled against."""',
            "",
        ]
        lines.extend(cls._version_guard())
        lines.extend([
            "",
            (
                "RPC_PYTHON_METHOD_NAMES: Final[MappingProxyType[str, str]] = "
                "MappingProxyType({"
            ),
            *(f'    "{wire}": "{python}",' for wire, python, *_rest in methods),
            "})",
            (
                '"""Wire RPC name to Python method name for the generated'
                ' service surface."""'
            ),
            "",
        ])
        lines.extend(cls._stub_class(service_full_name, methods))
        lines.extend(cls._servicer_class(methods))
        lines.extend(cls._registration(service_full_name, methods))
        lines.extend(
            cls._all_assignment([
                "FlextGrpcServiceServicer",
                "FlextGrpcServiceStub",
                "GRPC_GENERATED_VERSION",
                "RPC_PYTHON_METHOD_NAMES",
                "add_flext_grpc_service_servicer_to_server",
            ])
        )
        return "\n".join(lines) + "\n"

    @classmethod
    def _methods(
        cls,
        service: descriptor_pb2.ServiceDescriptorProto,
    ) -> tuple[tuple[str, str, str, str, bool, bool], ...]:
        """Plan one emission record per declared RPC.

        Args:
            service: The service carrying the RPC declarations.

        Returns:
            The ``(wire, python, input, output, client, server)`` records.

        """
        return tuple(
            (
                method.name,
                cls.python_method_name(method.name),
                cls._message_name(method.input_type),
                cls._message_name(method.output_type),
                method.client_streaming,
                method.server_streaming,
            )
            for method in service.method
        )

    @staticmethod
    def _message_name(qualified: str) -> str:
        """Resolve the Python message name of one qualified descriptor type.

        Args:
            qualified: The fully qualified descriptor type name.

        Returns:
            The unqualified Python message name.

        """
        return qualified.rsplit(".", maxsplit=1)[-1]

    @staticmethod
    def _version_guard() -> list[str]:
        """Render the typed runtime version guard without private imports.

        Returns:
            The rendered guard lines.

        """
        return [
            "",
            "def _installed_release_at_least(required: str) -> bool:",
            '    """Compare the installed ``grpcio`` release against ``required``.',
            "",
            "    Args:",
            "        required: The minimum release the surface was compiled for.",
            "",
            "    Returns:",
            "        Whether the installed release satisfies ``required``.",
            "",
            '    """',
            "    installed = tuple(",
            "        int(part)",
            '        for part in grpc.__version__.split(".")[:3]',
            "        if part.isdigit()",
            "    )",
            "    required_release = tuple(",
            '        int(part) for part in required.split(".")[:3] if part.isdigit()',
            "    )",
            "    return installed >= required_release",
            "",
            "",
            "if not _installed_release_at_least(GRPC_GENERATED_VERSION):",
            "    msg = (",
            '        f"The grpc package installed is at version {grpc.__version__}"',
            '        " but the generated code in flext_grpc/protos/flext_pb2_grpc.py"',
            '        " depends on the declared grpcio floor."',
            "    )",
            "    raise RuntimeError(msg)",
        ]

    @classmethod
    def _stub_class(
        cls,
        service_full_name: str,
        methods: tuple[tuple[str, str, str, str, bool, bool], ...],
    ) -> list[str]:
        """Render the typed client stub for the declared service.

        Args:
            service_full_name: The fully qualified service name.
            methods: The planned RPC emission records.

        Returns:
            The rendered stub class lines.

        """
        lines = [
            "",
            "",
            "class FlextGrpcServiceStub:",
            '    """Client stub for the generated service."""',
            "",
            "    def __init__(self, channel: grpc.Channel) -> None:",
            '        """Bind one multi-callable per RPC onto ``channel``.',
            "",
            "        Args:",
            "            channel: The channel carrying the service calls.",
            "",
            '        """',
        ]
        for (
            wire,
            python,
            request,
            response,
            client_streaming,
            server_streaming,
        ) in methods:
            kind = cls._CHANNEL_CALLS[client_streaming, server_streaming]
            serializer = f"flext_pb2.{request}.SerializeToString"
            lines.extend([
                (
                    f"        self.{python}: grpc."
                    f"{cls._CALLABLE_NAMES[client_streaming, server_streaming]}["
                ),
                f"            flext_pb2.{request},",
                f"            flext_pb2.{response},",
                f"        ] = channel.{kind}(",
                f'            "/{service_full_name}/{wire}",',
                f"            request_serializer={serializer},",
                f"            response_deserializer=flext_pb2.{response}.FromString,",
                "        )",
            ])
        return lines

    @classmethod
    def _servicer_class(
        cls,
        methods: tuple[tuple[str, str, str, str, bool, bool], ...],
    ) -> list[str]:
        """Render the typed servicer base for the declared service.

        Args:
            methods: The planned RPC emission records.

        Returns:
            The rendered servicer class lines.

        """
        lines = [
            "",
            "",
            "class FlextGrpcServiceServicer:",
            '    """Server base for the generated service."""',
        ]
        for wire, python, request, response, _client, _server in methods:
            lines.extend([
                "",
                "    @staticmethod",
                f"    def {python}(",
                f"        request: flext_pb2.{request},",
                "        context: grpc.ServicerContext,",
                f"    ) -> flext_pb2.{response}:",
                f'        """Report the ``{wire}`` RPC as unimplemented.',
                "",
                "        Args:",
                "            request: The decoded request message.",
                "            context: The servicer context of the call.",
                "",
                "        Raises:",
                "            NotImplementedError: Always, with the unimplemented",
                "                status set.",
                "",
                '        """',
                "        context.set_code(grpc.StatusCode.UNIMPLEMENTED)",
                '        context.set_details("Method not implemented!")',
                (
                    '        msg = f"Method not implemented! Request: '
                    '{type(request).__name__}"'
                ),
                "        raise NotImplementedError(msg)",
            ])
        return lines

    @classmethod
    def _registration(
        cls,
        service_full_name: str,
        methods: tuple[tuple[str, str, str, str, bool, bool], ...],
    ) -> list[str]:
        """Render the typed servicer registration function.

        Args:
            service_full_name: The fully qualified service name.
            methods: The planned RPC emission records.

        Returns:
            The rendered registration function lines.

        """
        lines = [
            "",
            "",
        ]
        for wire_, python, request, response, _client, _server in methods:
            lines.extend([
                (f"def _deserialize_{python}(payload: bytes) -> flext_pb2.{request}:"),
                f'    """Decode one ``{wire_}`` request payload.',
                "",
                "    Args:",
                "        payload: The serialized request bytes.",
                "",
                "    Returns:",
                f"        The decoded ``flext_pb2.{request}`` message.",
                "",
                '    """',
                f"    return flext_pb2.{request}.FromString(payload)",
                "",
                f"def _serialize_{python}(message: flext_pb2.{response}) -> bytes:",
                f'    """Encode one ``{wire_}`` response message.',
                "",
                "    Args:",
                "        message: The response message.",
                "",
                "    Returns:",
                "        The serialized response bytes.",
                "",
                '    """',
                "    return message.SerializeToString()",
                "",
            ])
        lines.extend([
            "def add_flext_grpc_service_servicer_to_server(",
            "    servicer: FlextGrpcServiceServicer,",
            "    server: grpc.Server,",
            ") -> None:",
            '    """Register the ``servicer`` RPC handlers with ``server``.',
            "",
            "    Args:",
            "        servicer: The servicer implementing the RPC methods.",
            "        server: The server receiving the handlers.",
            "",
            '    """',
            "    rpc_method_handlers = {",
        ])
        for (
            wire,
            python,
            _request,
            _response,
            client_streaming,
            server_streaming,
        ) in methods:
            factory = cls._HANDLER_FACTORIES[client_streaming, server_streaming]
            lines.extend([
                f'        "{wire}": grpc.{factory}(',
                f"            servicer.{python},",
                f"            request_deserializer=_deserialize_{python},",
                f"            response_serializer=_serialize_{python},",
                "        ),",
            ])
        lines.extend([
            "    }",
            "    generic_handler = grpc.method_handlers_generic_handler(",
            f'        "{service_full_name}",',
            "        rpc_method_handlers,",
            "    )",
            "    server.add_generic_rpc_handlers((generic_handler,))",
            "    server.add_registered_method_handlers(",
            f'        "{service_full_name}",',
            "        rpc_method_handlers,",
            "    )",
        ])
        return lines

    @staticmethod
    def _all_assignment(names: list[str]) -> list[str]:
        """Render the module export declaration for one projection.

        Args:
            names: The exported declaration names in emission order.

        Returns:
            The rendered ``__all__`` assignment lines.

        """
        return [
            "",
            "__all__: tuple[str, ...] = (",
            *(f'    "{name}",' for name in names),
            ")",
        ]

    @classmethod
    def _descriptor_assignment(cls, serialized: bytes) -> list[str]:
        """Render the descriptor assignment with lint-compliant line widths.

        Args:
            serialized: The serialized file descriptor.

        Returns:
            The rendered assignment lines.

        """
        width = cls._DESCRIPTOR_CHUNK_WIDTH
        chunks = [
            repr(serialized[start : start + width])
            for start in range(
                0,
                len(serialized),
                width,
            )
        ]
        lines = ["DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile("]
        lines.extend(f"    {chunk}" for chunk in chunks)
        lines.append(")")
        return lines

    @classmethod
    def _declared_floor(cls, distribution: str) -> tuple[int, int, int]:
        """Read the declared minimum release of one dependency from the manifest.

        The emitted version guards must compare against the declared dependency
        floor, never against whichever release happens to be importable in the
        generating environment; the manifest is the single source of truth.

        Args:
            distribution: The declared dependency name.

        Returns:
            The numeric floor prefix declared in the project manifest.

        Raises:
            ValueError: The manifest declares no floor for the distribution.

        """
        manifest = Path(__file__).resolve().parents[3] / "pyproject.toml"
        payload = tomllib.loads(manifest.read_text(encoding="utf-8"))
        requirements: list[str] = list(
            payload.get("project", {}).get("dependencies", []),
        )
        for group in (payload.get("dependency-groups") or {}).values():
            requirements.extend(group)
        for requirement in requirements:
            if not requirement.lower().startswith(f"{distribution.lower()}>="):
                continue
            floor = requirement.split(">=", 1)[1].split(",")[0].strip()
            parts = [int(part) for part in floor.split(".") if part.isdigit()]
            while len(parts) < cls._RELEASE_PART_COUNT:
                parts.append(0)
            return (parts[0], parts[1], parts[2])
        msg = f"Manifest declares no >= floor for {distribution}"
        raise ValueError(msg)

    @staticmethod
    def _projection_path(stem: str) -> Path:
        """Resolve one projection destination inside the protos package.

        Args:
            stem: The projection file name.

        Returns:
            The destination path.

        """
        return Path(__file__).resolve().parents[1] / "protos" / stem

    @classmethod
    def _module_name(cls, stem: str) -> str:
        """Resolve the importable module name of one projection destination.

        Args:
            stem: The projection file name.

        Returns:
            The dotted module name of the destination.

        """
        destination = cls._projection_path(stem)
        src_root = Path(__file__).resolve().parents[2]
        return (
            destination
            .relative_to(src_root)
            .with_suffix("")
            .as_posix()
            .replace(
                "/",
                ".",
            )
        )


__all__: list[str] = ["FlextGrpcUtilitiesSchemaCodegen"]
