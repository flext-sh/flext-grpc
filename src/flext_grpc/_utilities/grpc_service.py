"""Internal bindings between FLEXT models and the generated FlextGrpcService.

The generated ``protos/flext_pb2*.py`` modules are the only wire contract.
Message classes are resolved from the generated file descriptor, payloads are
parsed once at the protobuf boundary into the ``m.Grpc`` models, and the
untyped generated stub/registration API is reached only through a module
handle so every value crossing back is narrowed to a typed protobuf message.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING

from google.protobuf import json_format, message_factory
from google.protobuf.message import Message

from flext_core import r, u
from flext_grpc import c, m, p
from flext_grpc._utilities.grpc_runtime import FlextGrpcUtilitiesGrpcRuntime
from flext_grpc.protos import flext_pb2, flext_pb2_grpc

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from types import ModuleType

    from google.protobuf.descriptor import Descriptor, MethodDescriptor


class FlextGrpcUtilitiesGrpcService:
    """Typed client/server bindings over the generated FlextGrpcService code."""

    @staticmethod
    def _service_module() -> ModuleType:
        """Return the generated service module behind its untyped surface.

        Returns:
            The generated ``flext_pb2_grpc`` module.
        """
        return flext_pb2_grpc

    @staticmethod
    def method_descriptor(method: c.Grpc.ServiceMethod) -> MethodDescriptor:
        """Resolve one RPC of the generated service descriptor.

        Returns:
            The generated ``MethodDescriptor`` of ``method``.
        """
        service = flext_pb2.DESCRIPTOR.services_by_name[c.Grpc.SERVICE_PROTO_NAME]
        return service.methods_by_name[method.value]

    @staticmethod
    def encode_message(
        descriptor: Descriptor,
        model: m.BaseModel,
    ) -> p.Result[Message]:
        """Build the generated protobuf message carrying ``model``.

        Returns:
            The resulting ``p.Result[Message]``.
        """

        def _encode() -> Message:
            message_type = message_factory.GetMessageClass(descriptor)
            return json_format.ParseDict(model.model_dump(mode="json"), message_type())

        return u.try_(_encode, catch=(json_format.ParseError,))

    @staticmethod
    def decode_message[TModel: m.BaseModel](
        target: type[TModel],
        message: Message,
    ) -> p.Result[TModel]:
        """Parse a generated protobuf message into its FLEXT model once.

        Returns:
            The resulting ``p.Result[TModel]``.
        """
        return u.validate_value(
            target,
            json_format.MessageToJson(
                message,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True,
            ),
            from_json=True,
        )

    @staticmethod
    def invoke_unary[TModel: m.BaseModel](
        channel: p.Grpc.GrpcChannel,
        method: c.Grpc.ServiceMethod,
        request: m.BaseModel,
        response_type: type[TModel],
    ) -> p.Result[TModel]:
        """Call one unary RPC through the generated stub over ``channel``.

        Returns:
            The resulting ``p.Result[TModel]``.
        """
        descriptor = FlextGrpcUtilitiesGrpcService.method_descriptor(method)
        request_result = FlextGrpcUtilitiesGrpcService.encode_message(
            descriptor.input_type,
            request,
        )
        if request_result.failure:
            return r[TModel].from_failure(request_result)
        request_message = request_result.value
        stub = FlextGrpcUtilitiesGrpcService._service_module().FlextGrpcServiceStub(
            channel,
        )
        rpc = getattr(stub, method.value)

        def _call() -> Message:
            reply = rpc(request_message, timeout=c.Grpc.NETWORK_DEFAULT_TIMEOUT)
            if not isinstance(reply, Message):
                msg = f"{method.value} returned a non-protobuf reply"
                raise TypeError(msg)
            return reply

        reply_result = FlextGrpcUtilitiesGrpcRuntime.call_runtime(_call)
        if reply_result.failure:
            return r[TModel].fail_op(
                "gRPC call",
                FlextGrpcUtilitiesGrpcRuntime.runtime_failure_message(reply_result),
            )
        return FlextGrpcUtilitiesGrpcService.decode_message(
            response_type,
            reply_result.value,
        )

    @staticmethod
    def register_service(
        server: p.Grpc.GrpcServer,
        handlers: Mapping[
            c.Grpc.ServiceMethod,
            Callable[[Message, p.Grpc.GrpcServicerContext], Message],
        ],
    ) -> p.Result[bool]:
        """Register one handler per RPC through the generated registration.

        The generated ``add_..._to_server`` reads each RPC handler as an
        attribute named after the RPC, so the servicer is the attribute view
        of ``handlers`` keyed by ``c.Grpc.ServiceMethod`` values.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        missing = frozenset(c.Grpc.ServiceMethod).difference(handlers)
        if missing:
            return r[bool].fail(
                f"Missing RPC handlers: {sorted(method.value for method in missing)}",
            )
        servicer = SimpleNamespace(**{
            method.value: handler for method, handler in handlers.items()
        })
        service_module = FlextGrpcUtilitiesGrpcService._service_module()
        return FlextGrpcUtilitiesGrpcRuntime.run_runtime(
            lambda: service_module.add_FlextGrpcServiceServicer_to_server(
                servicer,
                server,
            ),
        )


__all__: list[str] = ["FlextGrpcUtilitiesGrpcService"]
