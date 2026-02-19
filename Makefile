# flext-grpc - gRPC Framework
PROJECT_NAME := flext-grpc
include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: proto proto-clean test-unit test-integration build shell

proto: ## Generate protobuf files
	$(Q)$(POETRY) run python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/*.proto

proto-clean: ## Clean generated protobuf files
	$(Q)find src -name "*_pb2*.py" -delete

.DEFAULT_GOAL := help
