import time

from timelimiter.event_loop import start_loop
from timelimiter.time_limiter import TimeLimiter
from timelimiter.timeout_handler import (
    TimeoutHandler,
    TimeoutHandlerFactory,
    TOTAL_HANDLER_COUNT,
)


class BenchmarkTimeHandler(TimeoutHandler):
    timeout = 1

    def _run(self):
        pass


class BenchmarkTimeHandlerFactory(TimeoutHandlerFactory):
    def create_handler(self) -> TimeoutHandler:
        return BenchmarkTimeHandler()


@TimeLimiter(BenchmarkTimeHandlerFactory())
def foo():
    pass


def benchmark():
    start = time.time()
    for _ in range(1_000_000):
        foo()
    duration = time.time() - start
    print(f"Loop a million times, cost: {duration} seconds")
    print(
        f"For one time, takes {duration * 1000 * 1000 / 1_000_000} microseconds"
    )
    while TOTAL_HANDLER_COUNT.val != 0:
        pass
    duration = time.time() - start
    print(f"All handler done, cost: {duration} seconds")
    print(
        f"For each handler, takes: {duration * 1000 * 1000 / 1_000_000} microseconds"
    )


if __name__ == "__main__":
    start_loop()
    benchmark()
