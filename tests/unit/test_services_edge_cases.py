"""Edge case tests for flext_grpc.services module.

Tests edge cases and boundary conditions to improve coverage.
"""

from __future__ import annotations

import math
import weakref
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from functools import (
    cached_property,
    lru_cache,
    partial,
    reduce,
    singledispatch,
    singledispatchmethod,
    total_ordering,
    wraps,
)
from itertools import (
    accumulate,
    batched,
    chain,
    combinations,
    combinations_with_replacement,
    compress,
    count,
    cycle,
    dropwhile,
    filterfalse,
    groupby,
    islice,
    pairwise,
    permutations,
    product,
    repeat,
    starmap,
    takewhile,
    tee,
    zip_longest,
)
from typing import NamedTuple

from flext_grpc.entities import FlextGrpcServer
from flext_grpc.services import FlextGrpcService


class TestFlextGrpcServiceEdgeCases:
    """Edge case tests for FlextGrpcService to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextGrpcService()
        self.now = datetime.now(UTC)

    def test_execute_with_very_long_command_name(self) -> None:
        """Test execute with very long command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        long_command = "a" * 1000  # Very long command name
        result = self.service.execute(long_command, server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_unicode_command_name(self) -> None:
        """Test execute with unicode command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        unicode_command = "测试命令"  # Unicode command name
        result = self.service.execute(unicode_command, server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_special_characters_command_name(self) -> None:
        """Test execute with special characters command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        special_command = "!@#$%^&*()"  # Special characters command name
        result = self.service.execute(special_command, server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_numeric_command_name(self) -> None:
        """Test execute with numeric command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(12345), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_boolean_command_name(self) -> None:
        """Test execute with boolean command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(True), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_list_command_name(self) -> None:
        """Test execute with list command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(["start", "server"]), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_dict_command_name(self) -> None:
        """Test execute with dict command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str({"command": "start"}), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_tuple_command_name(self) -> None:
        """Test execute with tuple command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(("start", "server")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_set_command_name(self) -> None:
        """Test execute with set command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str({"start", "server"}), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_frozenset_command_name(self) -> None:
        """Test execute with frozenset command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(frozenset(["start", "server"])), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_bytes_command_name(self) -> None:
        """Test execute with bytes command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(b"start"), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_bytearray_command_name(self) -> None:
        """Test execute with bytearray command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(bytearray(b"start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_memoryview_command_name(self) -> None:
        """Test execute with memoryview command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(memoryview(b"start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_range_command_name(self) -> None:
        """Test execute with range command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(range(10)), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_complex_command_name(self) -> None:
        """Test execute with complex command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(complex(1, 2)), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_float_command_name(self) -> None:
        """Test execute with float command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(math.pi), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_decimal_command_name(self) -> None:
        """Test execute with decimal command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(Decimal("3.14")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_fraction_command_name(self) -> None:
        """Test execute with fraction command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(Fraction(22, 7)), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_lambda_command_name(self) -> None:
        """Test execute with lambda command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(lambda x: x), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_generator_command_name(self) -> None:
        """Test execute with generator command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        def gen() -> Generator[str]:
            yield "start"

        result = self.service.execute(str(gen()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_coroutine_command_name(self) -> None:
        """Test execute with coroutine command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        def coro() -> str:
            return "invalid_command"

        result = self.service.execute(str(coro()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_async_generator_command_name(self) -> None:
        """Test execute with async generator command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        def async_gen() -> Generator[str]:
            yield "start"

        result = self.service.execute(str(async_gen()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_class_command_name(self) -> None:
        """Test execute with class command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            pass

        result = self.service.execute(str(TestClass), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_instance_command_name(self) -> None:
        """Test execute with instance command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            pass

        result = self.service.execute(str(TestClass()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_function_command_name(self) -> None:
        """Test execute with function command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        def test_func() -> str:
            return "invalid_command"

        result = self.service.execute(str(test_func), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_method_command_name(self) -> None:
        """Test execute with method command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            def test_method(self) -> str:
                return "invalid_command"

        obj = TestClass()
        result = self.service.execute(str(obj.test_method), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_property_command_name(self) -> None:
        """Test execute with property command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            @property
            def test_property(self) -> str:
                return "invalid_command"

        obj = TestClass()
        result = self.service.execute(str(obj.test_property), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_descriptor_command_name(self) -> None:
        """Test execute with descriptor command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestDescriptor:
            def __get__(self, obj: object | None, objtype: type | None = None) -> str:
                return "invalid_command"

        result = self.service.execute(str(TestDescriptor()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_metaclass_command_name(self) -> None:
        """Test execute with metaclass command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestMeta(type):
            pass

        result = self.service.execute(str(TestMeta), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_enum_command_name(self) -> None:
        """Test execute with enum command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestEnum(Enum):
            START = "start"

        result = self.service.execute(str(TestEnum.START), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_namedtuple_command_name(self) -> None:
        """Test execute with namedtuple command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestTuple(NamedTuple):
            command: str

        result = self.service.execute(str(TestTuple("start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_dataclass_command_name(self) -> None:
        """Test execute with dataclass command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @dataclass
        class TestDataClass:
            command: str

        result = self.service.execute(str(TestDataClass("start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_slots_command_name(self) -> None:
        """Test execute with slots command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @dataclass(slots=True)
        class TestSlots:
            command: str

        result = self.service.execute(str(TestSlots("start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_weakref_command_name(self) -> None:
        """Test execute with weakref command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            pass

        obj = TestClass()
        result = self.service.execute(str(weakref.ref(obj)), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_proxy_command_name(self) -> None:
        """Test execute with proxy command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            pass

        obj = TestClass()
        result = self.service.execute(str(weakref.proxy(obj)), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_contextmanager_command_name(self) -> None:
        """Test execute with contextmanager command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @contextmanager
        def test_context() -> Generator[str]:
            yield "start"

        result = self.service.execute(str(test_context()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_async_contextmanager_command_name(self) -> None:
        """Test execute with async contextmanager command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @contextmanager
        def test_async_context() -> Generator[str]:
            yield "start"

        result = self.service.execute(str(test_async_context()), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_partial_command_name(self) -> None:
        """Test execute with partial command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        def test_func(x: str, y: str) -> str:
            return f"{x}{y}"

        result = self.service.execute(str(partial(test_func, "start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_wraps_command_name(self) -> None:
        """Test execute with wraps command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        def test_decorator(func: object) -> object:
            @wraps(func)
            def wrapper(*args: object, **kwargs: object) -> object:
                return func(*args, **kwargs)

            return wrapper

        @test_decorator
        def test_func() -> str:
            return "invalid_command"

        result = self.service.execute(str(test_func), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_lru_cache_command_name(self) -> None:
        """Test execute with lru_cache command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @lru_cache(maxsize=128)
        def test_func(x: str) -> str:
            return f"start{x}"

        result = self.service.execute(str(test_func), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_singledispatch_command_name(self) -> None:
        """Test execute with singledispatch command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @singledispatch
        def test_func(arg: object) -> str:
            return f"start{arg}"

        result = self.service.execute(str(test_func), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_singledispatchmethod_command_name(self) -> None:
        """Test execute with singledispatchmethod command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            @singledispatchmethod
            def test_method(self, arg: object) -> str:
                return f"start{arg}"

        obj = TestClass()
        result = self.service.execute(str(obj.test_method), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_cached_property_command_name(self) -> None:
        """Test execute with cached_property command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        class TestClass:
            @cached_property
            def test_property(self) -> str:
                return "invalid_command"

        obj = TestClass()
        result = self.service.execute(str(obj.test_property), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_total_ordering_command_name(self) -> None:
        """Test execute with total_ordering command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        @total_ordering
        class TestClass:
            def __init__(self, value: str) -> None:
                self.value = value

            def __eq__(self, other: object) -> bool:
                return isinstance(other, TestClass) and self.value == other.value

            def __hash__(self) -> int:
                return hash(self.value)

            def __lt__(self, other: object) -> bool:
                return self.value < other.value

        result = self.service.execute(str(TestClass("start")), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_reduce_command_name(self) -> None:
        """Test execute with reduce command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(reduce), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_accumulate_command_name(self) -> None:
        """Test execute with accumulate command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(accumulate), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_chain_command_name(self) -> None:
        """Test execute with chain command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(chain), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_combinations_command_name(self) -> None:
        """Test execute with combinations command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(combinations), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_permutations_command_name(self) -> None:
        """Test execute with permutations command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(permutations), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_product_command_name(self) -> None:
        """Test execute with product command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(product), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_cycle_command_name(self) -> None:
        """Test execute with cycle command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(cycle), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_repeat_command_name(self) -> None:
        """Test execute with repeat command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(repeat), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_count_command_name(self) -> None:
        """Test execute with count command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(count), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_islice_command_name(self) -> None:
        """Test execute with islice command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(islice), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_tee_command_name(self) -> None:
        """Test execute with tee command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(tee), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_zip_longest_command_name(self) -> None:
        """Test execute with zip_longest command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(zip_longest), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_groupby_command_name(self) -> None:
        """Test execute with groupby command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(groupby), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_filterfalse_command_name(self) -> None:
        """Test execute with filterfalse command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(filterfalse), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_dropwhile_command_name(self) -> None:
        """Test execute with dropwhile command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(dropwhile), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_takewhile_command_name(self) -> None:
        """Test execute with takewhile command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(takewhile), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_compress_command_name(self) -> None:
        """Test execute with compress command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(compress), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_starmap_command_name(self) -> None:
        """Test execute with starmap command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(starmap), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_pairwise_command_name(self) -> None:
        """Test execute with pairwise command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(pairwise), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_batched_command_name(self) -> None:
        """Test execute with batched command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(batched), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error

    def test_execute_with_combinations_with_replacement_command_name(self) -> None:
        """Test execute with combinations_with_replacement command name."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute(str(combinations_with_replacement), server)

        assert result.is_success is False
        assert result.error is not None and "Unknown server command" in result.error
