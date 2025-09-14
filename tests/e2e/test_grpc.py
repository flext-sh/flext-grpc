"""End-to-end gRPC workflow tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import time

from flext_grpc import (
    FlextGrpcPlatform,
    FlextGrpcServerService,
    TGrpcTarget,
    create_client,
    create_complete_setup,
    create_config,
    create_server,
    create_service,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
    validate_address,
)

from .test_helpers import (
    assert_client_from_result,
    assert_client_from_setup,
    assert_server_from_result,
    assert_server_from_setup,
    assert_service_from_setup,
)

# Constants
EXPECTED_DATA_COUNT = 3


class TestCompleteGrpcWorkflow:
    """Test complete end-to-end gRPC workflows."""

    def test_enterprise_grpc_setup_workflow(self) -> None:
        """Test enterprise-grade gRPC setup workflow."""
        # 1. Validate addresses
        server_address = "localhost:9100"
        address_validation = validate_address(server_address)
        assert address_validation.success

        # 2. Create complete setup
        setup = create_complete_setup(
            "localhost",
            9100,
            "EnterpriseService",
            ["authenticate", "process_data", "get_status"],
        )

        # 3. Initialize platform
        platform = FlextGrpcPlatform()

        # 4. Start server with service - using DRY helper functions
        server_entity = assert_server_from_setup(setup)
        server_start = platform.start_server(server_entity)
        assert server_start.success
        running_server = assert_server_from_result(server_start.data)

        # Add service to server - using DRY helper functions
        service_entity = assert_service_from_setup(setup)
        service_add = platform.server_operation(
            "add_service",
            running_server,
            service=service_entity,
        )
        assert service_add.success
        server_with_service = service_add.data

        # 5. Connect client - using DRY helper functions
        client_entity = assert_client_from_setup(setup)
        client_connect = platform.connect_client(client_entity)
        assert client_connect.success
        connected_client = assert_client_from_result(client_connect.data)

        # 6. Execute enterprise workflow

        # Authentication
        auth_result = platform.make_call(
            connected_client,
            "authenticate",
            {"username": "enterprise_user", "token": "secure_token"},
        )
        assert auth_result.success
        assert auth_result.data is not None

        if not isinstance(auth_result.data, dict):
            raise TypeError(f"Expected dict, got {type(auth_result.data)}")
        auth_data = auth_result.data
        if auth_data["method"] != "authenticate":
            raise AssertionError(
                f"Expected {'authenticate'}, got {auth_data['method']}",
            )

        # Data processing
        process_result = platform.make_call(
            connected_client,
            "process_data",
            {
                "data": {"records": [1, 2, 3, 4, 5]},
                "processing_type": "batch",
                "priority": "high",
            },
        )
        assert process_result.success
        if process_result.data["method"] != "process_data":
            raise AssertionError(
                f"Expected {'process_data'}, got {process_result.data['method']}",
            )

        # Status check
        status_result = platform.make_call(
            connected_client,
            "get_status",
            {"request_id": "req_12345"},
        )
        assert status_result.success
        if status_result.data["method"] != "get_status":
            raise AssertionError(
                f"Expected {'get_status'}, got {status_result.data['method']}",
            )

        # 7. Server status verification
        final_status = platform.get_server_status(server_with_service)
        assert final_status.success
        status_data = final_status.data
        if status_data["address"] != "localhost:9100":
            raise AssertionError(
                f"Expected {'localhost:9100'}, got {status_data['address']}",
            )
        if not (status_data["is_running"]):
            raise AssertionError(f"Expected True, got {status_data['is_running']}")
        if status_data["service_count"] != 1:
            raise AssertionError(f"Expected {1}, got {status_data['service_count']}")

    def test_streaming_workflow(self) -> None:
        """Test complete streaming workflow."""
        platform = FlextGrpcPlatform()

        # 1. Setup server and client
        server = create_server("localhost", 9101)
        client = create_client("localhost:9101")

        # 2. Start server
        platform.start_server(server)

        # 3. Connect client
        client_result = platform.connect_client(client)
        connected_client = client_result.data

        # 4. Create different types of streams

        # Server streaming
        server_stream = platform.create_stream(
            connected_client,
            "server_data_stream",
            "server_streaming",
        )
        assert server_stream.success
        s_stream = server_stream.data
        assert s_stream.is_server_streaming
        assert not s_stream.is_client_streaming

        # Client streaming
        client_stream = platform.create_stream(
            connected_client,
            "client_upload_stream",
            "client_streaming",
        )
        assert client_stream.success
        c_stream = client_stream.data
        assert not c_stream.is_server_streaming
        assert c_stream.is_client_streaming

        # Bidirectional streaming
        bi_stream = platform.create_stream(
            connected_client,
            "bidirectional_chat",
            "bidirectional",
        )
        assert bi_stream.success
        b_stream = bi_stream.data
        assert b_stream.is_bidirectional

    def test_error_handling_workflow(self) -> None:
        """Test comprehensive error handling workflow."""
        platform = FlextGrpcPlatform()

        # 1. Test invalid server scenarios
        invalid_server = create_server("", 0)  # Invalid config

        start_result = platform.start_server(invalid_server)
        assert start_result.is_failure
        if "Invalid server" not in start_result.error:
            raise AssertionError(f"Expected {'Invalid server'} in {start_result.error}")

        # 2. Test invalid client scenarios
        invalid_client = create_client("invalid:address:format")

        # Client creation should still work (address validated later)
        platform.connect_client(invalid_client)
        # Connection might fail due to invalid target, but creation succeeds

        # 3. Test operation on non-running server
        valid_server = create_server("localhost", 9102)
        # Don't start server

        status_result = platform.get_server_status(valid_server)
        assert status_result.success  # Status check works even if not running
        status = status_result.data
        if status["is_running"]:
            raise AssertionError(f"Expected False, got {status['is_running']}")

    def test_multi_service_workflow(self) -> None:
        """Test workflow with multiple services."""
        platform = FlextGrpcPlatform()

        # 1. Create server
        server = create_server("localhost", 9103)
        start_result = platform.start_server(server)
        running_server = start_result.data

        # 2. Create multiple services
        auth_service = create_service("AuthService", ["login", "logout", "verify"])
        data_service = create_service(
            "DataService",
            ["create", "read", "update", "delete"],
        )
        notification_service = create_service(
            "NotificationService",
            ["send", "subscribe"],
        )

        # 3. Add all services to server
        for service in [auth_service, data_service, notification_service]:
            add_result = platform.server_operation(
                "add_service",
                running_server,
                service=service,
            )
            assert add_result.success
            running_server = add_result.data

        # 4. Verify all services are added
        final_status = platform.get_server_status(running_server)
        assert final_status.success
        if final_status.data["service_count"] != EXPECTED_DATA_COUNT:
            raise AssertionError(
                f"Expected {3}, got {final_status.data['service_count']}",
            )

        # 5. Create client and test each service
        client = create_client("localhost:9103")
        connect_result = platform.connect_client(client)
        connected_client = connect_result.data

        # Test auth service
        auth_call = platform.make_call(
            connected_client,
            "login",
            {"user": "test", "pass": "secret"},
        )
        assert auth_call.success
        if auth_call.data["method"] != "login":
            raise AssertionError(f"Expected {'login'}, got {auth_call.data['method']}")

        # Test data service
        data_call = platform.make_call(
            connected_client,
            "create",
            {"entity": "user", "data": {"name": "John"}},
        )
        assert data_call.success
        if data_call.data["method"] != "create":
            raise AssertionError(f"Expected {'create'}, got {data_call.data['method']}")

        # Test notification service
        notify_call = platform.make_call(
            connected_client,
            "send",
            {"recipient": "user@example.com", "message": "Hello"},
        )
        assert notify_call.success, "Notification call should succeed"
        if notify_call.data["method"] != "send":
            raise AssertionError(f"Expected {'send'}, got {notify_call.data['method']}")

    def test_configuration_driven_workflow(self) -> None:
        """Test configuration-driven workflow."""
        # 1. Create platform with custom configuration
        config = {
            "default_timeout": 60,
            "max_retries": 3,
            "compression": "gzip",
            "keepalive": True,
        }
        platform = FlextGrpcPlatform(config)

        # 2. Verify configuration is applied
        if platform.config != config:
            raise AssertionError(f"Expected {config}, got {platform.config}")

        # 3. Create services with configuration
        server = create_server("localhost", 9104, max_workers=20)
        client = create_client("localhost:9104", {"timeout": 60})

        # 4. Test that configured components work
        start_result = platform.start_server(server)
        assert start_result.success

        connect_result = platform.connect_client(client)
        assert connect_result.success

    def test_concurrent_clients_workflow(self) -> None:
        """Test workflow with concurrent clients."""
        platform = FlextGrpcPlatform()

        # 1. Setup server
        server = create_server("localhost", 9105)
        service = create_service("ConcurrentService", ["process"])

        start_result = platform.start_server(server)
        running_server = start_result.data

        add_service_result = platform.server_operation(
            "add_service",
            running_server,
            service=service,
        )
        server_with_service = add_service_result.data

        # 2. Create multiple clients
        clients = [create_client("localhost:9105") for _ in range(5)]

        # 3. Connect all clients
        connected_clients = []
        for client in clients:
            connect_result = platform.connect_client(client)
            assert connect_result.success
            connected_clients.append(connect_result.data)

        # 4. Make concurrent calls
        for i, client in enumerate(connected_clients):
            call_result = platform.make_call(
                client,
                "process",
                {"client_id": i, "data": f"data_{i}"},
            )
            assert call_result.success
            if call_result.data["data"]["client_id"] != i:
                raise AssertionError(
                    f"Expected {i}, got {call_result.data['data']['client_id']}",
                )

        # 5. Verify server handled all clients
        status_result = platform.get_server_status(server_with_service)
        assert status_result.success
        # Server should still be running and healthy

    def test_full_library_integration(self) -> None:
        """Test integration of all library components."""
        # Import everything to test no missing dependencies
        # All imports now at top of file

        # 1. Create using API functions
        server = create_server("localhost", 9106)
        client = create_client("localhost:9106")
        create_service("IntegrationTest", ["test"])
        create_config("localhost", 9106)

        # 2. Use platform for orchestration
        platform = FlextGrpcPlatform()

        # 3. Execute full workflow
        server_result = platform.start_server(server)
        client_result = platform.connect_client(client)

        assert server_result.success
        assert client_result.success

        # 4. Validate types work
        target_str = "localhost:9106"
        TGrpcTarget(target_str)
        # Imports now at top of file

        assert flext_grpc_validate_target(target_str)
        parsed = flext_grpc_parse_target(target_str)
        if parsed != ("localhost", 9106):
            raise AssertionError(f"Expected {('localhost', 9106)}, got {parsed}")

        # 5. Test service works
        app_service = FlextGrpcServerService()
        service_result = app_service.execute("status", server_result.data)
        assert service_result.success

    def test_performance_workflow(self) -> None:
        """Test basic performance characteristics."""
        platform = FlextGrpcPlatform()

        # 1. Measure server startup time
        server = create_server("localhost", 9107)

        start_time = time.time()
        start_result = platform.start_server(server)
        startup_time = time.time() - start_time

        assert start_result.success
        assert startup_time < 1.0  # Should start quickly

        # 2. Measure client connection time
        client = create_client("localhost:9107")

        connect_start = time.time()
        connect_result = platform.connect_client(client)
        connect_time = time.time() - connect_start

        assert connect_result.success
        assert connect_time < 1.0  # Should connect quickly

        # 3. Measure call performance
        connected_client = connect_result.data

        call_times = []
        for i in range(10):
            call_start = time.time()
            call_result = platform.make_call(
                connected_client,
                "perf_test",
                {"iteration": i},
            )
            call_time = time.time() - call_start
            call_times.append(call_time)

            assert call_result.success

        # Average call time should be reasonable
        avg_call_time = sum(call_times) / len(call_times)
        assert avg_call_time < 0.1  # Calls should be fast
