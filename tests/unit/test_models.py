"""Behavioral tests for flext_grpc.models public contract.

Asserts observable behavior only: field defaults, validators, computed
fields, immutability, and the r[T] outcomes of model methods and state
transitions. No private attribute access, no internal spying.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pydantic
import pytest
from flext_tests import tm

from tests import m


class TestsFlextGrpcModelsUnit:
    """Behavioral contract tests for FlextGrpcModels.Grpc models."""

    # ------------------------------------------------------------------
    # Value message models: field contract, defaults, immutability
    # ------------------------------------------------------------------

    @staticmethod
    def test_echo_request_exposes_message() -> None:
        """EchoRequest carries the provided message on its public field."""
        request = m.Grpc.EchoRequest(message="ping")

        tm.that(request.message, eq="ping")

    @staticmethod
    def test_echo_response_defaults_server_id_and_message() -> None:
        """EchoResponse defaults server_id to empty and keeps the message."""
        response = m.Grpc.EchoResponse(message="pong")

        tm.that(response.message, eq="pong")
        tm.that(response.server_id, eq="")

    @staticmethod
    def test_health_response_defaults_message_empty() -> None:
        """HealthResponse requires status and defaults message to empty."""
        response = m.Grpc.HealthResponse(status="SERVING")

        tm.that(response.status, eq="SERVING")
        tm.that(response.message, eq="")

    @staticmethod
    def test_value_model_is_immutable() -> None:
        """Value models are frozen: assigning a field raises ValidationError."""
        request = m.Grpc.EchoRequest(message="x")

        with pytest.raises(pydantic.ValidationError):
            request.message = "y"

    # ------------------------------------------------------------------
    # StreamInfo: validation via model_validate and numeric constraints
    # ------------------------------------------------------------------

    @staticmethod
    def test_stream_info_model_validate_populates_fields() -> None:
        """StreamInfo.model_validate maps the input payload onto public fields."""
        info = m.Grpc.StreamInfo.model_validate({
            "stream_id": "s1",
            "stream_type": "unary",
            "target": "localhost:50051",
        })

        tm.that(info.stream_id, eq="s1")
        tm.that(info.stream_type, eq="unary")
        tm.that(info.target, eq="localhost:50051")

    @staticmethod
    def test_stream_info_defaults_counters_to_zero() -> None:
        """StreamInfo defaults its counters and latency to zero."""
        info = m.Grpc.StreamInfo(stream_id="s", stream_type="unary", target="t")

        tm.that(info.total_requests_sent, eq=0)
        tm.that(info.error_count, eq=0)
        tm.that(info.average_latency_ms, eq=0.0)

    @staticmethod
    @pytest.mark.parametrize("field", ["total_requests_sent", "error_count"])
    def test_stream_info_rejects_negative_counters(field: str) -> None:
        """Non-negative counter constraints reject negative values."""
        with pytest.raises(pydantic.ValidationError):
            m.Grpc.StreamInfo.model_validate({
                "stream_id": "s",
                "stream_type": "unary",
                "target": "t",
                field: -1,
            })

    # ------------------------------------------------------------------
    # Config models: default contract
    # ------------------------------------------------------------------

    @staticmethod
    def test_client_config_uses_provided_target_and_timeout() -> None:
        """ClientConfig stores the target and timeout it is given."""
        config = m.Grpc.ClientConfig(target="127.0.0.1:50051", timeout=30.0)

        tm.that(config.target, eq="127.0.0.1:50051")
        tm.that(config.timeout, eq=30.0)

    @staticmethod
    def test_client_config_applies_defaults() -> None:
        """ClientConfig exposes a concrete default target endpoint."""
        config = m.Grpc.ClientConfig()

        tm.that(config.target, eq="127.0.0.1:50051")

    @staticmethod
    def test_channel_config_defaults_options_to_none() -> None:
        """ChannelConfig keeps the address and defaults options to None."""
        config = m.Grpc.ChannelConfig(address="localhost:50051")

        tm.that(config.address, eq="localhost:50051")
        tm.that(config.options, eq=None)

    # ------------------------------------------------------------------
    # OperationSpec / Request / Response: validators and computed fields
    # ------------------------------------------------------------------

    @staticmethod
    def test_operation_spec_rejects_blank_name() -> None:
        """OperationSpec strips and rejects whitespace-only names."""
        with pytest.raises(pydantic.ValidationError):
            m.Grpc.OperationSpec(name="   ", entity_type="server")

    @staticmethod
    def test_request_valid_true_for_named_operation() -> None:
        """Request.valid computed field is True when the operation is named."""
        request = m.Grpc.Request(
            operation=m.Grpc.OperationSpec(name="op", entity_type="server"),
        )

        tm.that(request.valid, eq=True)

    @staticmethod
    @pytest.mark.parametrize(
        ("success", "error", "expected"),
        [
            (True, None, False),
            (False, None, True),
            (True, "boom", True),
            (False, "boom", True),
        ],
    )
    def test_response_has_error_reflects_success_and_error(
        *,
        success: bool,
        error: str | None,
        expected: bool,
    ) -> None:
        """Response.has_error is True on failure or whenever an error is set."""
        response = m.Grpc.Response(success=success, error=error)

        tm.that(response.has_error, eq=expected)

    # ------------------------------------------------------------------
    # Payload: value normalization contract
    # ------------------------------------------------------------------

    @staticmethod
    def test_payload_from_values_normalizes_none_and_complex() -> None:
        """from_values maps None to "" and stringifies non-primitive values."""
        payload = m.Grpc.Payload.from_values(missing=None, count=1, items=[1, 2])

        values = dict(payload.values)
        tm.that(values["missing"], eq="")
        tm.that(values["count"], eq=1)
        tm.that(values["items"], eq="[1, 2]")

    # ------------------------------------------------------------------
    # StateMachine: transition returns r[T] with correct outcome
    # ------------------------------------------------------------------

    @staticmethod
    def test_state_machine_allows_permitted_transition() -> None:
        """A permitted transition succeeds and reports the target state."""
        machine = m.Grpc.StateMachine()

        result = machine.transition("idle", "ready", {"idle": {"ready"}})

        tm.that(result.success, eq=True)
        tm.that(result.unwrap().state, eq="ready")

    @staticmethod
    def test_state_machine_rejects_disallowed_transition() -> None:
        """A disallowed transition fails with a descriptive error."""
        machine = m.Grpc.StateMachine()

        result = machine.transition("idle", "running", {"idle": {"ready"}})

        tm.that(result.success, eq=False)
        tm.that(result.error, none=False)
        tm.that(result.error, has="running")

    # ------------------------------------------------------------------
    # Channel: lifecycle transitions and business-rule validation
    # ------------------------------------------------------------------

    @staticmethod
    def test_channel_connect_advances_to_connecting() -> None:
        """connect() from idle succeeds and yields a connecting channel."""
        channel = m.Grpc.Channel(target="localhost:50051")

        result = channel.connect()

        tm.that(result.success, eq=True)
        tm.that(result.unwrap().state, eq="connecting")

    @staticmethod
    def test_channel_mark_ready_requires_connecting_first() -> None:
        """mark_ready() fails from idle but succeeds after connect()."""
        channel = m.Grpc.Channel(target="localhost:50051")

        tm.that(channel.mark_ready().success, eq=False)

        connecting = channel.connect().unwrap()
        ready = connecting.mark_ready()
        tm.that(ready.success, eq=True)
        tm.that(ready.unwrap().ready(), eq=True)

    @staticmethod
    def test_channel_rejects_empty_target_business_rule() -> None:
        """validate_business_rules fails for a blank channel target."""
        channel = m.Grpc.Channel(target="   ")

        result = channel.validate_business_rules()

        tm.that(result.success, eq=False)

    @staticmethod
    def test_channel_accepts_valid_target_business_rule() -> None:
        """validate_business_rules succeeds for a non-empty target."""
        channel = m.Grpc.Channel(target="localhost:50051")

        tm.that(channel.validate_business_rules().success, eq=True)

    # ------------------------------------------------------------------
    # Server: lifecycle transitions and validation
    # ------------------------------------------------------------------

    @staticmethod
    def test_server_start_transitions_to_starting() -> None:
        """start() from stopped succeeds and yields a starting server."""
        server = m.Grpc.Server(host="localhost", port=50051)

        result = server.start()

        tm.that(result.success, eq=True)
        tm.that(result.unwrap().state, eq="starting")

    @staticmethod
    def test_server_mark_stopped_fails_when_not_running() -> None:
        """mark_stopped() is rejected from a stopped state."""
        server = m.Grpc.Server(host="localhost", port=50051)

        tm.that(server.mark_stopped().success, eq=False)

    @staticmethod
    def test_server_rejects_blank_host_business_rule() -> None:
        """validate_business_rules fails when the bind host is blank."""
        server = m.Grpc.Server(host="   ", port=50051)

        tm.that(server.validate_business_rules().success, eq=False)

    @staticmethod
    def test_server_accepts_valid_configuration() -> None:
        """validate_business_rules succeeds for a well-formed server."""
        server = m.Grpc.Server(host="localhost", port=50051)

        tm.that(server.validate_business_rules().success, eq=True)

    # ------------------------------------------------------------------
    # Service: field validators and functional method management
    # ------------------------------------------------------------------

    @staticmethod
    def test_service_rejects_empty_name() -> None:
        """Service name validator rejects a blank name."""
        with pytest.raises(pydantic.ValidationError):
            m.Grpc.Service(name="", methods=("a",))

    @staticmethod
    def test_service_rejects_empty_methods() -> None:
        """Service methods validator rejects an empty method tuple."""
        with pytest.raises(pydantic.ValidationError):
            m.Grpc.Service(name="svc", methods=())

    @staticmethod
    def test_service_add_method_appends_new_and_rejects_duplicate() -> None:
        """add_method appends a new method and refuses duplicates."""
        service = m.Grpc.Service(name="svc", methods=("a",))

        added = service.add_method("b")
        tm.that(added.success, eq=True)
        tm.that(added.unwrap().methods, has="b")

        tm.that(service.add_method("a").success, eq=False)

    @staticmethod
    def test_service_has_method_reflects_membership() -> None:
        """has_method reports whether a method name is registered."""
        service = m.Grpc.Service(name="svc", methods=("a",))

        tm.that(service.has_method("a"), eq=True)
        tm.that(service.has_method("z"), eq=False)

    # ------------------------------------------------------------------
    # Client / GrpcStream: connect delegation and validators
    # ------------------------------------------------------------------

    @staticmethod
    def test_client_connect_to_creates_channel_for_target() -> None:
        """connect_to attaches a channel bound to the requested target."""
        result = m.Grpc.Client().connect_to("localhost:50051")

        tm.that(result.success, eq=True)
        client = result.unwrap()
        channel = tm.not_none(client.channel)
        tm.that(channel.target, eq="localhost:50051")

    @staticmethod
    def test_grpc_stream_rejects_blank_method_name() -> None:
        """GrpcStream method_name validator rejects whitespace-only names."""
        with pytest.raises(pydantic.ValidationError):
            m.Grpc.GrpcStream(method_name="   ")
