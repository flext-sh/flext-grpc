# Private project handlers for flext-grpc.
# Strict extension: only `_custom_<verb>_<what>` handlers and `(pre|post)-<verb>[-<what>]`
# hooks. Public targets, toolchain vars, .DEFAULT_GOAL, includes, and help are
# invalid (base.mk owns those). Invoke via `make run WHAT=<what>`.
.PHONY: _custom_run_proto _custom_run_proto-clean
_custom_run_proto: ## make run WHAT=proto — generate protobuf files
	$(Q)$(POETRY) run python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/*.proto
_custom_run_proto-clean: ## make run WHAT=proto-clean — remove generated protobuf files
	$(Q)find src -name "*_pb2*.py" -delete
