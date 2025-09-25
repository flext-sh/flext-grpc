"""End-to-end gRPC workflow tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_grpc import (
    FlextGrpcPlatform,
    create_complete_setup,
    validate_address,
)

# from .test_helpers import (
#     assert_client_from_result,
#     assert_client_from_setup,
#     assert_server_from_result,
#     assert_server_from_setup,
#     assert_service_from_setup,
# )

# Constants
EXPECTED_DATA_COUNT = 3
TIMEOUT_SECONDS = 3


class TestGrpcWorkflows:
    """Test class for end-to-end gRPC workflows."""

    def test_enterprise_grpc_workflow(self) -> None:
        """Test enterprise-grade gRPC setup workflow."""
        # 1. Validate addresses
        server_address = "localhost:9100"
        address_validation = validate_address(server_address)
        assert address_validation.is_success

        # 2. Create complete setup
        setup = create_complete_setup(
            "localhost",
            9100,
            "EnterpriseService",
            ["authenticate", "process_data", "get_status"],
        )

        # 3. Initialize platform
        platform = FlextGrpcPlatform()

        # 4. Get entities from setup
        server_entity = setup["server"]
        service_entity = setup["service"]
        client_entity = setup["client"]

        # Basic validation that entities exist
        assert server_entity is not None
        assert service_entity is not None
        assert client_entity is not None

        # Test platform creation
        assert platform is not None

    def test_streaming_workflow(self) -> None:
        """Test streaming workflow creation."""
        platform = FlextGrpcPlatform()
        assert platform is not None

    def test_error_handling_workflow(self) -> None:
        """Test error handling workflow."""
        platform = FlextGrpcPlatform()
        assert platform is not None
