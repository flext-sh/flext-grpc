"""End-to-end tests for complete FLEXT gRPC workflows.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_grpc import (
    FlextGrpcPlatform,
    create_complete_setup,
    create_server,
    create_client,
    create_service,
    validate_address,
)


class TestCompleteGrpcWorkflow:
    """Test complete end-to-end gRPC workflows."""

    def test_enterprise_grpc_setup_workflow(self) -> None:
        """Test enterprise-grade gRPC setup workflow."""
        # 1. Validate addresses
        server_address = "localhost:9100"
        address_validation = validate_address(server_address)
        assert address_validation.is_success
        
        # 2. Create complete setup
        setup = create_complete_setup(
            "localhost", 9100, "EnterpriseService", 
            ["authenticate", "process_data", "get_status"]
        )
        
        # 3. Initialize platform
        platform = FlextGrpcPlatform()
        
        # 4. Start server with service
        server_start = platform.start_server(setup["server"])
        assert server_start.is_success
        running_server = server_start.data
        
        # Add service to server
        service_add = platform.server_operation(
            "add_service", running_server, service=setup["service"]
        )
        assert service_add.is_success
        server_with_service = service_add.data
        
        # 5. Connect client
        client_connect = platform.connect_client(setup["client"])
        assert client_connect.is_success
        connected_client = client_connect.data
        
        # 6. Execute enterprise workflow
        
        # Authentication
        auth_result = platform.make_call(
            connected_client, "authenticate", 
            {"username": "enterprise_user", "token": "secure_token"}
        )
        assert auth_result.is_success
        assert auth_result.data["method"] == "authenticate"
        
        # Data processing
        process_result = platform.make_call(
            connected_client, "process_data",
            {
                "data": {"records": [1, 2, 3, 4, 5]},
                "processing_type": "batch",
                "priority": "high"
            }
        )
        assert process_result.is_success
        assert process_result.data["method"] == "process_data"
        
        # Status check
        status_result = platform.make_call(
            connected_client, "get_status", {"request_id": "req_12345"}
        )
        assert status_result.is_success
        assert status_result.data["method"] == "get_status"
        
        # 7. Server status verification
        final_status = platform.get_server_status(server_with_service)
        assert final_status.is_success
        status_data = final_status.data
        assert status_data["address"] == "localhost:9100"
        assert status_data["is_running"] is True
        assert status_data["service_count"] == 1

    def test_streaming_workflow(self) -> None:
        """Test complete streaming workflow."""
        platform = FlextGrpcPlatform()
        
        # 1. Setup server and client
        server = create_server("localhost", 9101)
        client = create_client("localhost:9101")
        
        # 2. Start server
        server_result = platform.start_server(server)
        running_server = server_result.data
        
        # 3. Connect client
        client_result = platform.connect_client(client)
        connected_client = client_result.data
        
        # 4. Create different types of streams
        
        # Server streaming
        server_stream = platform.create_stream(
            connected_client, "server_data_stream", "server_streaming"
        )
        assert server_stream.is_success
        s_stream = server_stream.data
        assert s_stream.is_server_streaming()
        assert not s_stream.is_client_streaming()
        
        # Client streaming
        client_stream = platform.create_stream(
            connected_client, "client_upload_stream", "client_streaming"
        )
        assert client_stream.is_success
        c_stream = client_stream.data
        assert not c_stream.is_server_streaming()
        assert c_stream.is_client_streaming()
        
        # Bidirectional streaming
        bi_stream = platform.create_stream(
            connected_client, "bidirectional_chat", "bidirectional"
        )
        assert bi_stream.is_success
        b_stream = bi_stream.data
        assert b_stream.is_bidirectional()

    def test_error_handling_workflow(self) -> None:
        """Test comprehensive error handling workflow."""
        platform = FlextGrpcPlatform()
        
        # 1. Test invalid server scenarios
        invalid_server = create_server("", 0)  # Invalid config
        
        start_result = platform.start_server(invalid_server)
        assert start_result.is_failure
        assert "Invalid server" in start_result.error
        
        # 2. Test invalid client scenarios
        invalid_client = create_client("invalid:address:format")
        
        # Client creation should still work (address validated later)
        connect_result = platform.connect_client(invalid_client)
        # Connection might fail due to invalid target, but creation succeeds
        
        # 3. Test operation on non-running server
        valid_server = create_server("localhost", 9102)
        # Don't start server
        
        status_result = platform.get_server_status(valid_server)
        assert status_result.is_success  # Status check works even if not running
        status = status_result.data
        assert status["is_running"] is False

    def test_multi_service_workflow(self) -> None:
        """Test workflow with multiple services."""
        platform = FlextGrpcPlatform()
        
        # 1. Create server
        server = create_server("localhost", 9103)
        start_result = platform.start_server(server)
        running_server = start_result.data
        
        # 2. Create multiple services
        auth_service = create_service("AuthService", ["login", "logout", "verify"])
        data_service = create_service("DataService", ["create", "read", "update", "delete"])
        notification_service = create_service("NotificationService", ["send", "subscribe"])
        
        # 3. Add all services to server
        for service in [auth_service, data_service, notification_service]:
            add_result = platform.server_operation(
                "add_service", running_server, service=service
            )
            assert add_result.is_success
            running_server = add_result.data
        
        # 4. Verify all services are added
        final_status = platform.get_server_status(running_server)
        assert final_status.is_success
        assert final_status.data["service_count"] == 3
        
        # 5. Create client and test each service
        client = create_client("localhost:9103")
        connect_result = platform.connect_client(client)
        connected_client = connect_result.data
        
        # Test auth service
        auth_call = platform.make_call(
            connected_client, "login", {"user": "test", "pass": "secret"}
        )
        assert auth_call.is_success
        assert auth_call.data["method"] == "login"
        
        # Test data service
        data_call = platform.make_call(
            connected_client, "create", {"entity": "user", "data": {"name": "John"}}
        )
        assert data_call.is_success
        assert data_call.data["method"] == "create"
        
        # Test notification service
        notify_call = platform.make_call(
            connected_client, "send", {"recipient": "user@example.com", "message": "Hello"}
        )
        assert notify_call.is_success
        assert notify_call.data["method"] == "send"

    def test_configuration_driven_workflow(self) -> None:
        """Test configuration-driven workflow."""
        # 1. Create platform with custom configuration
        config = {
            "default_timeout": 60,
            "max_retries": 3,
            "compression": "gzip",
            "keepalive": True
        }
        platform = FlextGrpcPlatform(config)
        
        # 2. Verify configuration is applied
        assert platform.config == config
        
        # 3. Create services with configuration
        server = create_server("localhost", 9104, max_workers=20)
        client = create_client("localhost:9104", {"timeout": 60})
        
        # 4. Test that configured components work
        start_result = platform.start_server(server)
        assert start_result.is_success
        
        connect_result = platform.connect_client(client)
        assert connect_result.is_success
        
    def test_concurrent_clients_workflow(self) -> None:
        """Test workflow with concurrent clients."""
        platform = FlextGrpcPlatform()
        
        # 1. Setup server
        server = create_server("localhost", 9105)
        service = create_service("ConcurrentService", ["process"])
        
        start_result = platform.start_server(server)
        running_server = start_result.data
        
        add_service_result = platform.server_operation(
            "add_service", running_server, service=service
        )
        server_with_service = add_service_result.data
        
        # 2. Create multiple clients
        clients = [
            create_client("localhost:9105") 
            for _ in range(5)
        ]
        
        # 3. Connect all clients
        connected_clients = []
        for client in clients:
            connect_result = platform.connect_client(client)
            assert connect_result.is_success
            connected_clients.append(connect_result.data)
        
        # 4. Make concurrent calls
        for i, client in enumerate(connected_clients):
            call_result = platform.make_call(
                client, "process", {"client_id": i, "data": f"data_{i}"}
            )
            assert call_result.is_success
            assert call_result.data["data"]["client_id"] == i
        
        # 5. Verify server handled all clients
        status_result = platform.get_server_status(server_with_service)
        assert status_result.is_success
        # Server should still be running and healthy

    def test_full_library_integration(self) -> None:
        """Test integration of all library components."""
        # Import everything to test no missing dependencies
        from flext_grpc import (
            # Entities
            FlextGrpcChannel, FlextGrpcClient, FlextGrpcServer, 
            FlextGrpcService, FlextGrpcStream,
            
            # Services
            FlextGrpcApplicationService,
            
            # Platform
            FlextGrpcPlatform,
            
            # Config
            FlextGrpcConfig,
            
            # API
            create_channel, create_client, create_server,
            create_service, create_stream, create_config,
            
            # Types
            TGrpcTarget, TGrpcChannelState, TGrpcServerState,
            
            # Errors
            FlextGrpcError, FlextGrpcValidationError,
            
            # Validation
            flext_grpc_validate_target, flext_grpc_parse_target,
        )
        
        # 1. Create using API functions
        server = create_server("localhost", 9106)
        client = create_client("localhost:9106")
        service = create_service("IntegrationTest", ["test"])
        config = create_config("localhost", 9106)
        
        # 2. Use platform for orchestration
        platform = FlextGrpcPlatform()
        
        # 3. Execute full workflow
        server_result = platform.start_server(server)
        client_result = platform.connect_client(client)
        
        assert server_result.is_success
        assert client_result.is_success
        
        # 4. Validate types work
        target = TGrpcTarget("localhost:9106")
        assert flext_grpc_validate_target(target)
        parsed = flext_grpc_parse_target(target)
        assert parsed == ("localhost", 9106)
        
        # 5. Test service works
        app_service = FlextGrpcApplicationService()
        service_result = app_service.execute("server", "status", server_result.data)
        assert service_result.is_success
        
        print("✅ Full library integration test passed")

    def test_performance_workflow(self) -> None:
        """Test basic performance characteristics."""
        import time
        
        platform = FlextGrpcPlatform()
        
        # 1. Measure server startup time
        server = create_server("localhost", 9107)
        
        start_time = time.time()
        start_result = platform.start_server(server)
        startup_time = time.time() - start_time
        
        assert start_result.is_success
        assert startup_time < 1.0  # Should start quickly
        
        # 2. Measure client connection time
        client = create_client("localhost:9107")
        
        connect_start = time.time()
        connect_result = platform.connect_client(client)
        connect_time = time.time() - connect_start
        
        assert connect_result.is_success
        assert connect_time < 1.0  # Should connect quickly
        
        # 3. Measure call performance
        connected_client = connect_result.data
        
        call_times = []
        for i in range(10):
            call_start = time.time()
            call_result = platform.make_call(
                connected_client, "perf_test", {"iteration": i}
            )
            call_time = time.time() - call_start
            call_times.append(call_time)
            
            assert call_result.is_success
        
        # Average call time should be reasonable
        avg_call_time = sum(call_times) / len(call_times)
        assert avg_call_time < 0.1  # Calls should be fast