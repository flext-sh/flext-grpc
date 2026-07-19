.PHONY: proto
proto: ## Regenerate Python gRPC modules from protos/*.proto (grpc_tools.protoc)
	$(Q)$(POETRY) run python -m grpc_tools.protoc \
		--proto_path=src \
		--python_out=src \
		--grpc_python_out=src \
		src/flext_grpc/protos/flext.proto
	$(Q)$(POETRY) run ruff check --fix --select I src/flext_grpc/protos/flext_pb2.py src/flext_grpc/protos/flext_pb2_grpc.py
	$(Q)$(POETRY) run ruff format src/flext_grpc/protos/flext_pb2.py src/flext_grpc/protos/flext_pb2_grpc.py

.DEFAULT_GOAL := help
