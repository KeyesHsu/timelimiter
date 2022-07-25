import functools
import os

from timelimiter.event_loop import is_loop_running
from timelimiter.exceptions import (
    TimeoutHandlerFactoryMissingException,
    TimeLimiterFullException,
)
from timelimiter.timeout_handler import (
    register_handler,
    TOTAL_HANDLER_COUNT,
    TimeoutHandlerFactory,
)

TIME_LIMITER_CAPACITY = int(os.getenv("TIME_LIMITER_CAPACITY") or 100_000)


class TimeLimiter:
    """Time limiter decorator

    Typical uses of this class take the following form:

        @TimeLimiter(MySQLTimeoutHandler)
        def foo():
            # Do something
            ...
    """

    def __init__(self, handler_factory: TimeoutHandlerFactory):
        if not handler_factory:
            raise TimeoutHandlerFactoryMissingException(
                f"Missing timeout handler factory"
            )
        self._handler_factory = handler_factory

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            # Just return if loop is not running
            if not is_loop_running():
                return func(*args, **kwargs)

            if TOTAL_HANDLER_COUNT.val >= TIME_LIMITER_CAPACITY:
                return self.reject_strategy()

            # Dynamic create handler, due to some data we can only get in the
            # main thread, mysql thread id for example.
            # Create handler and register handler to be run.
            handler = self._handler_factory.create_handler()
            register_handler(handler)

            try:
                # Run actually function
                result = func(*args, **kwargs)
            finally:
                # Cancel timeout handler after func run
                handler.cancel()
            return result

        return _wrapper

    def reject_strategy(self):
        """Reject strategy when total handler count reaches the limit
        """
        raise TimeLimiterFullException(
            f"Total handler count[{TOTAL_HANDLER_COUNT.val}] reaches the "
            f"limit[{TIME_LIMITER_CAPACITY}]"
        )
