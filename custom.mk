# Private project handlers for flext-grpc.
# Strict extension: only `_custom_<verb>_<what>` handlers and `(pre|post)-<verb>[-<what>]`
# hooks. Public targets, toolchain vars, .DEFAULT_GOAL, includes, and help are
# invalid (base.mk owns those). Each handler maps to `make <verb> WHAT=<what>`.
.PHONY: _custom_build_proto _custom_clean_proto
_custom_build_proto: ## make build WHAT=proto — generate protobuf files
	$(Q)$(POETRY) run python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/*.proto
_custom_clean_proto: ## make clean WHAT=proto — remove generated protobuf files
	$(Q)find src -name "*_pb2*.py" -delete
