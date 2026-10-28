"""Internal bindings between FLEXT models and the generated FlextGrpcService.

The generated ``protos/flext_pb2*.py`` modules are the only wire contract.
Message classes are resolved from the generated file descriptor, payloads are
parsed once at the protobuf boundary into the ``m.Grpc`` models, and every
value crossing back is narrowed to a typed protobuf message. The generated
stub and registration surface is typed by the wire-schema compiler; the
Python RPC names are reached through its emitted wire-to-Python name
projection.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, override

import grpc
from flext_core import u
from google.protobuf import json_format, message_factory
from google.protobuf.descriptor import Descriptor, MethodDescriptor, ServiceDescriptor
from google.protobuf.message import Message

from flext_grpc import c, m, p, r
from flext_grpc._utilities import FlextGrpcUtilitiesGrpcRuntime
from flext_grpc.protos import flext_pb2, flext_pb2_grpc

if TYPE_CHECKING:
    from collections.abc import Callable


class FlextGrpcUtilitiesGrpcService:
    """Typed client/server bindings over the generated FlextGrpcService code."""

    class _HandlerServicer(flext_pb2_grpc.FlextGrpcServiceServicer):
        """Servicer view of the registered RPC handlers."""

        def __init__(
            self,
            handlers: Mapping[
                c.Grpc.ServiceMethod,
                Callable[[Message, p.Grpc.GrpcServicerContext], Message],
            ],
        ) -> None:
            """Store one handler per RPC.

            Args:
                handlers: The RPC handlers keyed by service method.

            """
            self._handlers = handlers

        @override
        def echo(
            self,
            request: flext_pb2.EchoRequest,
            context: grpc.ServicerContext,
        ) -> flext_pb2.EchoResponse:
            """Handle ``Echo`` through its registered handler.

            Args:
                request: The decoded request message.
                context: The servicer context of the call.

            Returns:
                The narrowed handler reply.

            """
            return self._reply(
                self._handlers[c.Grpc.ServiceMethod.ECHO](request, context),
                flext_pb2.EchoResponse,
            )

        @override
        def health_check(
            self,
            request: flext_pb2.HealthRequest,
            context: grpc.ServicerContext,
        ) -> flext_pb2.HealthResponse:
            """Handle ``HealthCheck`` through its registered handler.

            Args:
                request: The decoded request message.
                context: The servicer context of the call.

            Returns:
                The narrowed handler reply.

            """
            return self._reply(
                self._handlers[c.Grpc.ServiceMethod.HEALTH_CHECK](request, context),
                flext_pb2.HealthResponse,
            )

        @staticmethod
        def _reply[ResponseT: Message](
            reply: Message,
            expected: type[ResponseT],
        ) -> ResponseT:
            """Narrow one handler reply to the declared protobuf message type.

            Args:
                reply: The raw handler reply.
                expected: The message type declared for the RPC.

            Returns:
                The narrowed reply.

            Raises:
                TypeError: If the handler returned a different message type.

            """
            if not isinstance(reply, expected):
                msg = (
                    f"RPC handler returned {type(reply).__name__},"
                    f" expected {expected.__name__}"
                )
                raise TypeError(msg)
            return reply

    @staticmethod
    def method_descriptor(method: c.Grpc.ServiceMethod) -> MethodDescriptor:
        """Resolve one RPC of the generated service descriptor.

        Returns:
            The generated ``MethodDescriptor`` of ``method``.

        """
        service: ServiceDescriptor = flext_pb2.DESCRIPTOR.services_by_name[
            c.Grpc.SERVICE_PROTO_NAME
        ]
        resolved: MethodDescriptor = service.methods_by_name[method.value]
        return resolved

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
            built: Message = json_format.ParseDict(
                model.model_dump(mode="json"),
                message_type(),
            )
            return built

        return u.try_(_encode, catch=(json_format.ParseError, TypeError))

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
        if not isinstance(channel, grpc.Channel):
            return r[TModel].fail(
                "Channel does not implement the grpc.Channel contract",
            )
        request_message = request_result.value
        stub = flext_pb2_grpc.FlextGrpcServiceStub(channel)
        rpc = getattr(
            stub,
            flext_pb2_grpc.RPC_PYTHON_METHOD_NAMES[method.value],
        )

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

        The generated ``add_..._to_server`` reads each RPC handler as the
        snake-case Python projection of the RPC name; the servicer bridges
        the handlers keyed by ``c.Grpc.ServiceMethod`` onto those names and
        narrows each reply to the declared protobuf message type.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        missing = frozenset(c.Grpc.ServiceMethod).difference(handlers)
        if missing:
            return r[bool].fail(
                f"Missing RPC handlers: {sorted(method.value for method in missing)}",
            )
        if not isinstance(server, grpc.Server):
            return r[bool].fail(
                "Server does not implement the grpc.Server contract",
            )
        servicer = FlextGrpcUtilitiesGrpcService._HandlerServicer(handlers)
        return FlextGrpcUtilitiesGrpcRuntime.run_runtime(
            lambda: flext_pb2_grpc.add_flext_grpc_service_servicer_to_server(
                servicer,
                server,
            ),
        )


__all__: list[str] = ["FlextGrpcUtilitiesGrpcService"]
