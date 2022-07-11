import random
import time
from concurrent.futures import wait, thread

from timelimiter.counter import Counter
from timelimiter.event_loop import start_loop
from timelimiter.time_limiter import TimeLimiter
from timelimiter.timeout_handler import (
    TimeoutHandler,
    TimeoutHandlerFactory,
    TimeoutHandlerState,
)

total_count = 1000
run_counter = Counter()
cancel_counter = Counter()


def print_count():
    print(f"Total count: {total_count}")
    print(f"Run count: {run_counter.val}")
    print(f"Cancel count: {cancel_counter.val}")


def reset_count():
    run_counter.reset()
    cancel_counter.reset()


class ManualTestTimeHandler(TimeoutHandler):
    def __init__(self):
        super(ManualTestTimeHandler, self).__init__()
        # Random set timeout from 100ms to 300ms
        self.timeout = random.randint(1, 3) * 0.1

    def _run(self):
        run_counter.inc()

    def cancel(self):
        super(ManualTestTimeHandler, self).cancel()
        if self._state == TimeoutHandlerState.CANCELLED:
            cancel_counter.inc()


class ManualTestTimeHandlerFactory(TimeoutHandlerFactory):
    def create_handler(self) -> TimeoutHandler:
        return ManualTestTimeHandler()


@TimeLimiter(ManualTestTimeHandlerFactory())
def foo():
    # Sleep 200ms
    time.sleep(0.2)


class ManualTestTimeLimiter:
    @classmethod
    def test(cls):
        """Run total count times and judge the run count and cancel count
        """
        reset_count()
        for _ in range(total_count):
            foo()

        print_count()
        assert total_count == run_counter.val + cancel_counter.val

    @classmethod
    def multiprocess_test(cls):
        """Multiprocess run total count times and judge the run count and cancel
            count
        """
        reset_count()
        with thread.ThreadPoolExecutor(max_workers=5) as executor:
            fs = [executor.submit(foo) for _ in range(total_count)]
            wait(fs)

        print_count()
        assert total_count == run_counter.val + cancel_counter.val


if __name__ == "__main__":
    start_loop()
    ManualTestTimeLimiter.test()
    ManualTestTimeLimiter.multiprocess_test()
