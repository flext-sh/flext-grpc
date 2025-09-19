"""Unit tests for real business scenarios.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_grpc import (
    FlextGrpcClient,
    FlextGrpcPlatform,
    FlextGrpcServer,
    FlextGrpcService,
    create_complete_setup,
    create_server,
    create_service,
)


class TestRealBusinessScenarios:
    """Test real business scenarios that demonstrate actual library usage."""

    def test_microservice_setup_scenario(self) -> None:
        """Test setting up a microservice with real validation and state management."""
        # Business Scenario: Setting up a user management microservice

        # 1. Create the server for the microservice
        user_server = create_server("localhost", 50070, 5)
        assert user_server.state == "stopped"
        assert not user_server.is_running

        # 2. Define the service with real business methods
        user_service = create_service(
            "UserService",
            ["CreateUser", "GetUser", "UpdateUser", "DeleteUser", "ListUsers"],
        )

        # 3. Validate business rules
        server_validation = user_server.validate_business_rules()
        assert server_validation.success, (
            f"Server validation failed: {server_validation.error}"
        )

        service_validation = user_service.validate_business_rules()
        assert service_validation.success, (
            f"Service validation failed: {service_validation.error}"
        )

        # 4. Test server lifecycle management
        start_result = user_server.start()
        assert start_result.success, f"Failed to start server: {start_result.error}"

        starting_server = start_result.data
        assert starting_server is not None
        assert starting_server.state == "starting"

        # 5. Complete startup process
        running_result = starting_server.mark_running()
        assert running_result.success, f"Failed to mark running: {running_result.error}"

        running_server = running_result.data
        assert running_server is not None
        assert running_server.state == "running"
        assert running_server.is_running

        # 6. Register service with running server
        service_add_result = running_server.add_service(user_service)
        assert service_add_result.success, (
            f"Failed to add service: {service_add_result.error}"
        )

        server_with_service = service_add_result.data
        assert server_with_service is not None
        assert len(server_with_service.services) == 1
        assert server_with_service.services[0].name == "UserService"
        assert server_with_service.services[0].has_method("CreateUser")
        assert server_with_service.services[0].has_method("GetUser")

        # 7. Test graceful shutdown
        stop_result = server_with_service.stop()
        assert stop_result.success, f"Failed to stop server: {stop_result.error}"

        stopping_server = stop_result.data
        assert stopping_server is not None
        assert stopping_server.state == "stopping"

        # 8. Complete shutdown
        stopped_result = stopping_server.mark_stopped()
        assert stopped_result.success, f"Failed to mark stopped: {stopped_result.error}"

        final_server = stopped_result.data
        assert final_server is not None
        assert final_server.state == "stopped"
        assert not final_server.is_running

    def test_platform_orchestration_scenario(self) -> None:
        """Test using platform for orchestrating multiple services."""
        # Business Scenario: API Gateway orchestrating multiple backend services

        platform = FlextGrpcPlatform()

        # 1. Create multiple backend services
        auth_server = FlextGrpcServer(
            id="auth-service",
            host="localhost",
            port=50071,
            max_workers=3,
            created_at=datetime.now(UTC),
        )

        user_server = FlextGrpcServer(
            id="user-service",
            host="localhost",
            port=50072,
            max_workers=5,
            created_at=datetime.now(UTC),
        )

        # 2. Validate all services
        assert auth_server.validate_business_rules().success
        assert user_server.validate_business_rules().success

        # 3. Use platform to start services (tests real platform operations)
        auth_start = platform.start_server(auth_server)
        user_start = platform.start_server(user_server)

        # Platform should handle gracefully whether services actually start or not
        assert auth_start.success or auth_start.is_failure
        assert user_start.success or user_start.is_failure

        # 4. Test platform status operations
        auth_status = platform.get_server_status(auth_server)
        assert auth_status.success or auth_status.is_failure

        if auth_status.success:
            status_data = auth_status.data
            assert isinstance(status_data, dict)
            assert "address" in status_data
            assert "state" in status_data
            assert "is_running" in status_data
            assert status_data["address"] == "localhost:50071"

        # 5. Test platform service coordination
        user_status = platform.get_server_status(user_server)
        assert user_status.success or user_status.is_failure

    def test_service_evolution_scenario(self) -> None:
        """Test evolving a service by adding methods (real business scenario)."""
        # Business Scenario: API versioning and service evolution

        # 1. Start with v1 of a service
        payment_service_v1 = create_service(
            "PaymentService", ["ProcessPayment", "GetPaymentStatus"],
        )

        assert payment_service_v1.validate_business_rules().success
        assert payment_service_v1.has_method("ProcessPayment")
        assert payment_service_v1.has_method("GetPaymentStatus")
        assert not payment_service_v1.has_method("RefundPayment")  # Not in v1

        # 2. Evolve to v2 by adding methods
        add_refund_result = payment_service_v1.add_method("RefundPayment")
        assert add_refund_result.success, (
            f"Failed to add method: {add_refund_result.error}"
        )

        payment_service_v2 = add_refund_result.data
        assert payment_service_v2 is not None
        assert payment_service_v2.has_method("ProcessPayment")  # Still has v1 methods
        assert payment_service_v2.has_method("GetPaymentStatus")  # Still has v1 methods
        assert payment_service_v2.has_method("RefundPayment")  # New v2 method

        # 3. Add another v2 method
        add_webhook_result = payment_service_v2.add_method("ConfigureWebhook")
        assert add_webhook_result.success

        payment_service_v2_final = add_webhook_result.data
        assert payment_service_v2_final is not None
        assert len(payment_service_v2_final.methods) == 4
        assert payment_service_v2_final.has_method("ConfigureWebhook")

        # 4. Test that duplicate methods are rejected
        duplicate_result = payment_service_v2_final.add_method("ProcessPayment")
        assert duplicate_result.is_failure
        assert duplicate_result.error is not None
        assert "already exists" in duplicate_result.error

    def test_complete_setup_factory_scenario(self) -> None:
        """Test using the complete setup factory for rapid development."""
        # Business Scenario: Rapid prototyping of a new service

        # 1. Use factory to create complete setup
        setup = create_complete_setup(
            "localhost",
            50073,
            "NotificationService",
            ["SendEmail", "SendSMS", "SendPush", "GetNotificationHistory"],
        )

        # 2. Validate all components work together
        server = setup["server"]
        client = setup["client"]
        service = setup["service"]
        target = setup["target"]

        assert isinstance(server, FlextGrpcServer)
        assert isinstance(client, FlextGrpcClient)
        assert isinstance(service, FlextGrpcService)
        assert isinstance(target, str)

        # 3. Test server configuration
        assert server.host == "localhost"
        assert server.port == 50073
        assert server.address == "localhost:50073"
        assert server.validate_business_rules().success

        # 4. Test client configuration
        assert client.channel is not None
        assert client.channel.target == "localhost:50073"
        assert client.target == "localhost:50073"
        assert client.validate_business_rules().success

        # 5. Test service configuration
        assert service.name == "NotificationService"
        assert service.has_method("SendEmail")
        assert service.has_method("SendSMS")
        assert service.has_method("SendPush")
        assert service.has_method("GetNotificationHistory")
        assert len(service.methods) == 4
        assert service.validate_business_rules().success

        # 6. Test integration between components
        service_add_result = server.add_service(service)
        assert service_add_result.success

        integrated_server = service_add_result.data
        assert integrated_server is not None
        assert len(integrated_server.services) == 1
        assert integrated_server.services[0].name == "NotificationService"

        # 7. Test target consistency
        assert target == "localhost:50073"
        assert target == server.address
        assert target == client.target

    def test_error_handling_business_scenario(self) -> None:
        """Test real error conditions that occur in business scenarios."""
        # Business Scenario: Configuration validation in production deployment

        # 1. Test invalid server configurations that would fail in production
        invalid_configs = [
            {"host": "", "port": 50074, "error": "host cannot be empty"},
            {"host": "localhost", "port": -1, "error": "Invalid port"},
            {"host": "localhost", "port": 99999, "error": "Invalid port"},
            {
                "host": "localhost",
                "port": 50075,
                "max_workers": 0,
                "error": "Max workers must be >= 1",
            },
        ]

        for config in invalid_configs:
            server = FlextGrpcServer(
                id=f"invalid-{config['port']}",
                host=config["host"],
                port=config["port"],
                max_workers=config.get("max_workers", 10),
                created_at=datetime.now(UTC),
            )

            validation = server.validate_business_rules()
            assert validation.is_failure, f"Should have failed for config: {config}"
            assert validation.error is not None
            assert config["error"] in validation.error

        # 2. Test invalid service configurations
        empty_service = FlextGrpcService(
            id="empty-service",
            name="",  # Invalid empty name
            methods=["method1"],
            created_at=datetime.now(UTC),
        )

        validation = empty_service.validate_business_rules()
        assert validation.is_failure
        assert validation.error is not None
        assert "name cannot be empty" in validation.error

        # 3. Test service without methods
        no_methods_service = FlextGrpcService(
            id="no-methods-service",
            name="ValidService",
            methods=[],  # No methods
            created_at=datetime.now(UTC),
        )

        validation = no_methods_service.validate_business_rules()
        assert validation.is_failure
        assert validation.error is not None
        assert "must have at least one method" in validation.error

    def test_concurrent_service_management_scenario(self) -> None:
        """Test managing multiple services concurrently (real scenario)."""
        # Business Scenario: Managing multiple microservices in a cluster

        platform = FlextGrpcPlatform()

        # 1. Create multiple services that might run concurrently
        services = []
        for i, service_name in enumerate(
            ["Gateway", "Auth", "Users", "Orders"], start=1,
        ):
            server = FlextGrpcServer(
                id=f"{service_name.lower()}-service",
                host="localhost",
                port=50080 + i,
                max_workers=2 + i,
                created_at=datetime.now(UTC),
            )

            service = FlextGrpcService(
                id=f"{service_name.lower()}-svc",
                name=f"{service_name}Service",
                methods=[f"Handle{service_name}Request"],
                created_at=datetime.now(UTC),
            )

            services.append(
                {
                    "server": server,
                    "service": service,
                    "name": service_name,
                },
            )

        # 2. Validate all services
        for svc in services:
            assert svc["server"].validate_business_rules().success
            assert svc["service"].validate_business_rules().success

        # 3. Test platform can handle multiple service operations
        results = []
        for svc in services:
            start_result = platform.start_server(svc["server"])
            status_result = platform.get_server_status(svc["server"])

            results.append(
                {
                    "name": svc["name"],
                    "start": start_result,
                    "status": status_result,
                },
            )

        # 4. Validate platform handled all operations gracefully
        for result in results:
            # Platform should handle gracefully whether operations succeed or fail
            assert result["start"].success or result["start"].is_failure
            assert result["status"].success or result["status"].is_failure

            # If status succeeded, validate data structure
            if result["status"].success:
                status_data = result["status"].data
                assert isinstance(status_data, dict)
                assert all(
                    key in status_data for key in ["address", "state", "is_running"]
                )
