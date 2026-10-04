"""Behavioral unit tests for the gRPC error hierarchy.

Exercises the public contract of ``FlextGrpcErrors``: raisability, message
propagation via ``str(error)``, the public ``field`` / ``config_key`` state,
and the semantic inheritance each specialized error promises (validation,
connection, timeout, configuration).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest
from flext_tests import e, tm

from flext_grpc.errors import FlextGrpcErrors


class TestsFlextGrpcErrors:
    """Behavioral contract for the FlextGrpcErrors exception family."""

    def test_base_error_carries_message_and_raises(self) -> None:
        """Error propagates its message and is catchable as the core base."""
        message = "Base gRPC error occurred"
        with pytest.raises(e.BaseError) as caught:
            raise FlextGrpcErrors.Error(message)
        tm.that(str(caught.value), has=message)

    @pytest.mark.parametrize(
        ("factory", "message"),
        [
            (FlextGrpcErrors.Error, "base failure"),
            (FlextGrpcErrors.ValidationError, "invalid request"),
            (FlextGrpcErrors.GrpcConnectionError, "channel down"),
            (FlextGrpcErrors.GrpcTimeoutError, "deadline exceeded"),
            (FlextGrpcErrors.ConfigurationError, "bad settings"),
        ],
    )
    def test_every_error_raises_as_base_and_reports_message(
        self, factory: type[Exception], message: str
    ) -> None:
        """Each error is raisable, an Exception, and echoes its message."""
        with pytest.raises(e.BaseError) as caught:
            raise factory(message)
        tm.that(caught.value, is_=Exception)
        tm.that(str(caught.value), has=message)

    @pytest.mark.parametrize(
        ("factory", "semantic_parent"),
        [
            (FlextGrpcErrors.ValidationError, e.ValidationError),
            (FlextGrpcErrors.GrpcConnectionError, e.ConnectionError),
            (FlextGrpcErrors.GrpcTimeoutError, e.TimeoutError),
            (FlextGrpcErrors.ConfigurationError, e.ConfigurationError),
        ],
    )
    def test_specialized_error_keeps_its_semantic_category(
        self, factory: type[Exception], semantic_parent: type[Exception]
    ) -> None:
        """A specialized error is-a its core semantic category, not a sibling."""
        error = factory("boom")
        tm.that(error, is_=semantic_parent)

    def test_connection_error_is_not_a_validation_error(self) -> None:
        """Distinct categories do not collapse: a connection error is not validation."""
        message = "channel down"
        with pytest.raises(e.ConnectionError) as caught:
            raise FlextGrpcErrors.GrpcConnectionError(message)
        assert not isinstance(caught.value, e.ValidationError)

    @pytest.mark.parametrize("field", ["username", "データ", None])
    def test_validation_error_exposes_field_state(self, field: str | None) -> None:
        """ValidationError publishes the field it was constructed with."""
        error = FlextGrpcErrors.ValidationError("Invalid field value", field=field)
        tm.that(str(error), has="Invalid field value")
        if field is None:
            tm.that(error.field, none=True)
        else:
            tm.that(error.field, eq=field)

    def test_validation_error_field_defaults_to_none(self) -> None:
        """ValidationError omitting field reports None, not a fabricated value."""
        error = FlextGrpcErrors.ValidationError("General validation error")
        tm.that(error.field, none=True)

    @pytest.mark.parametrize("config_key", ["port", "complex_setting", None])
    def test_configuration_error_exposes_config_key_state(
        self, config_key: str | None
    ) -> None:
        """ConfigurationError publishes the config_key it was constructed with."""
        error = FlextGrpcErrors.ConfigurationError(
            "Invalid configuration", config_key=config_key
        )
        tm.that(str(error), has="Invalid configuration")
        if config_key is None:
            tm.that(error.config_key, none=True)
        else:
            tm.that(error.config_key, eq=config_key)

    def test_configuration_error_config_key_defaults_to_none(self) -> None:
        """ConfigurationError omitting config_key reports None."""
        error = FlextGrpcErrors.ConfigurationError("Configuration error")
        tm.that(error.config_key, none=True)
