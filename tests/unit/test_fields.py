"""Tests for flext_grpc.fields module.

Tests the field validation functions for gRPC entities.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo

from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.fields import (
    grpc_host_field,
    grpc_method_name_field,
    grpc_port_field,
    grpc_service_name_field,
    grpc_timeout_field,
    grpc_workers_field,
)


class TestGrpcFields:
    """Test gRPC field validation functions."""

    def test_grpc_host_field_valid(self) -> None:
        """Test grpc_host_field with valid values."""
        field = grpc_host_field()
        assert isinstance(field, FieldInfo)

        # Test with valid host
        class TestModel(BaseModel):
            host: str = grpc_host_field()

        model = TestModel(host="localhost")
        assert model.host == "localhost"

        model = TestModel(host="example.com")
        assert model.host == "example.com"

        model = TestModel(host="192.168.1.1")
        assert model.host == "192.168.1.1"

    def test_grpc_host_field_invalid(self) -> None:
        """Test grpc_host_field with invalid values."""

        class TestModel(BaseModel):
            host: str = grpc_host_field()

        # Test empty host
        with pytest.raises(ValidationError) as exc_info:
            TestModel(host="")
        assert "String should have at least 1 character" in str(exc_info.value)

        # Test invalid characters
        with pytest.raises(ValidationError) as exc_info:
            TestModel(host="invalid@host")
        assert "String should match pattern" in str(exc_info.value)

        # Test too long host
        with pytest.raises(ValidationError) as exc_info:
            TestModel(host="a" * 256)
        assert "String should have at most 255 characters" in str(exc_info.value)

    def test_grpc_port_field_valid(self) -> None:
        """Test grpc_port_field with valid values."""
        field = grpc_port_field()
        assert isinstance(field, FieldInfo)

        class TestModel(BaseModel):
            port: int = grpc_port_field()

        model = TestModel(port=8080)
        assert model.port == 8080

        model = TestModel(port=1024)
        assert model.port == 1024

        model = TestModel(port=65535)
        assert model.port == 65535

    def test_grpc_port_field_invalid(self) -> None:
        """Test grpc_port_field with invalid values."""

        class TestModel(BaseModel):
            port: int = grpc_port_field()

        # Test port too low
        with pytest.raises(ValidationError) as exc_info:
            TestModel(port=1023)
        assert "Input should be greater than or equal to 1024" in str(exc_info.value)

        # Test port too high
        with pytest.raises(ValidationError) as exc_info:
            TestModel(port=65536)
        assert "Input should be less than or equal to 65535" in str(exc_info.value)

    def test_grpc_service_name_field_valid(self) -> None:
        """Test grpc_service_name_field with valid values."""
        field = grpc_service_name_field()
        assert isinstance(field, FieldInfo)

        class TestModel(BaseModel):
            service_name: str = grpc_service_name_field()

        model = TestModel(service_name="UserService")
        assert model.service_name == "UserService"

        model = TestModel(service_name="user_service")
        assert model.service_name == "user_service"

        model = TestModel(service_name="user.service")
        assert model.service_name == "user.service"

    def test_grpc_service_name_field_invalid(self) -> None:
        """Test grpc_service_name_field with invalid values."""

        class TestModel(BaseModel):
            service_name: str = grpc_service_name_field()

        # Test empty service name
        with pytest.raises(ValidationError) as exc_info:
            TestModel(service_name="")
        assert "String should have at least 1 character" in str(exc_info.value)

        # Test invalid start character
        with pytest.raises(ValidationError) as exc_info:
            TestModel(service_name="1Service")
        assert "String should match pattern" in str(exc_info.value)

        # Test invalid end character
        with pytest.raises(ValidationError) as exc_info:
            TestModel(service_name="Service_")
        assert "String should match pattern" in str(exc_info.value)

    def test_grpc_method_name_field_valid(self) -> None:
        """Test grpc_method_name_field with valid values."""
        field = grpc_method_name_field()
        assert isinstance(field, FieldInfo)

        class TestModel(BaseModel):
            method_name: str = grpc_method_name_field()

        model = TestModel(method_name="GetUser")
        assert model.method_name == "GetUser"

        model = TestModel(method_name="get_user")
        assert model.method_name == "get_user"

        model = TestModel(method_name="getUser")
        assert model.method_name == "getUser"

    def test_grpc_method_name_field_invalid(self) -> None:
        """Test grpc_method_name_field with invalid values."""

        class TestModel(BaseModel):
            method_name: str = grpc_method_name_field()

        # Test empty method name
        with pytest.raises(ValidationError) as exc_info:
            TestModel(method_name="")
        assert "String should have at least 1 character" in str(exc_info.value)

        # Test invalid start character
        with pytest.raises(ValidationError) as exc_info:
            TestModel(method_name="1Method")
        assert "String should match pattern" in str(exc_info.value)

        # Test invalid character
        with pytest.raises(ValidationError) as exc_info:
            TestModel(method_name="method.name")
        assert "String should match pattern" in str(exc_info.value)

    def test_grpc_timeout_field_valid(self) -> None:
        """Test grpc_timeout_field with valid values."""
        field = grpc_timeout_field()
        assert isinstance(field, FieldInfo)

        class TestModel(BaseModel):
            timeout: float = grpc_timeout_field()

        model = TestModel(timeout=30.0)
        assert model.timeout == 30.0

        model = TestModel(timeout=0.1)
        assert model.timeout == 0.1

        model = TestModel(timeout=3600.0)
        assert model.timeout == 3600.0

    def test_grpc_timeout_field_invalid(self) -> None:
        """Test grpc_timeout_field with invalid values."""

        class TestModel(BaseModel):
            timeout: float = grpc_timeout_field()

        # Test timeout too low
        with pytest.raises(ValidationError) as exc_info:
            TestModel(timeout=0.0)
        assert "Input should be greater than 0" in str(exc_info.value)

        # Test timeout too high
        with pytest.raises(ValidationError) as exc_info:
            TestModel(timeout=3601.0)
        assert "Input should be less than or equal to 3600" in str(exc_info.value)

    def test_grpc_workers_field_valid(self) -> None:
        """Test grpc_workers_field with valid values."""
        field = grpc_workers_field()
        assert isinstance(field, FieldInfo)

        class TestModel(BaseModel):
            workers: int = grpc_workers_field()

        model = TestModel(workers=1)
        assert model.workers == 1

        model = TestModel(workers=10)
        assert model.workers == 10

        model = TestModel(workers=1000)
        assert model.workers == 1000

    def test_grpc_workers_field_invalid(self) -> None:
        """Test grpc_workers_field with invalid values."""

        class TestModel(BaseModel):
            workers: int = grpc_workers_field()

        # Test workers too low
        with pytest.raises(ValidationError) as exc_info:
            TestModel(workers=0)
        assert "Input should be greater than or equal to 1" in str(exc_info.value)

        # Test workers too high
        with pytest.raises(ValidationError) as exc_info:
            TestModel(workers=1001)
        assert "Input should be less than or equal to 1000" in str(exc_info.value)

    def test_field_defaults(self) -> None:
        """Test that fields have correct default values."""
        # Test host field default
        host_field = grpc_host_field()
        assert host_field.default == FlextGrpcConstants.GRPC_DEFAULT_HOST

        # Test port field default
        port_field = grpc_port_field()
        assert port_field.default == FlextGrpcConstants.GRPC_DEFAULT_PORT

        # Test timeout field default
        timeout_field = grpc_timeout_field()
        assert timeout_field.default == FlextGrpcConstants.GRPC_DEFAULT_TIMEOUT

        # Test workers field default
        workers_field = grpc_workers_field()
        assert workers_field.default == 10
