import time
from unittest import TestCase

from timelimiter.event_loop import start_loop
from timelimiter.exceptions import (
    TimeLimiterFullException,
    TimeoutHandlerFactoryMissingException,
)
from timelimiter import time_limiter
from timelimiter.time_limiter import TimeLimiter
from timelimiter.timeout_handler import TimeoutHandler, TimeoutHandlerFactory

_result = None


class CapacityChanger:
    def __int__(self):
        self.origin_capacity = None

    def __enter__(self):
        self.origin_capacity = time_limiter.TIME_LIMITER_CAPACITY
        time_limiter.TIME_LIMITER_CAPACITY = 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        time_limiter.TIME_LIMITER_CAPACITY = self.origin_capacity


class MySQLTimeoutHandler(TimeoutHandler):
    timeout = 0.5

    def __init__(self):
        super(MySQLTimeoutHandler, self).__init__()
        self.thread_id = 1

    def _run(self):
        global _result
        _result = "Timeout"


class MySQLTimeoutHandlerFactory(TimeoutHandlerFactory):
    def create_handler(self) -> TimeoutHandler:
        return MySQLTimeoutHandler()


class TestTimeLimiter(TestCase):
    def test_time_limiter(self):
        # Start event loop
        start_loop()
        factory = MySQLTimeoutHandlerFactory()

        @TimeLimiter(factory)
        def foo():
            time.sleep(0.1)

        # Assert foo does not time out
        foo()
        self.assertIsNone(_result)

        @TimeLimiter(factory)
        def bar():
            time.sleep(1)

        # Test timeout 0.5s, func run 1s
        bar()
        self.assertEqual("Timeout", _result)

    def test_time_limiter_capacity(self):
        factory = MySQLTimeoutHandlerFactory()

        @TimeLimiter(factory)
        def foo():
            time.sleep(0.1)

        # Test handler count reaches the limit
        with CapacityChanger():
            with self.assertRaisesRegex(
                TimeLimiterFullException, "reaches the limit"
            ):
                foo()

    def test_loop_is_not_running(self):
        # Do not start loop

        factory = MySQLTimeoutHandlerFactory()

        @TimeLimiter(factory)
        def foo():
            pass

        # Test handler count reaches the limit
        with CapacityChanger():
            foo()

    def test_without_factory(self):
        with self.assertRaisesRegex(
            TimeoutHandlerFactoryMissingException,
            "Missing timeout handler factory",
        ):

            @TimeLimiter(None)
            def foo():
                pass
