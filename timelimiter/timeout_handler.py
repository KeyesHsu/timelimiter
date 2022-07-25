from asyncio import Handle
from enum import Enum, auto
from timelimiter.counter import Counter
from timelimiter.exceptions import RepetitiveScheduledException

TOTAL_HANDLER_COUNT = Counter(0)


class TimeoutHandlerState(Enum):
    def _generate_next_value_(name, start, count, last_values):  # noqa
        return name

    CREATED = auto()
    SCHEDULED = auto()
    RUNNING = auto()
    DONE = auto()
    FAILED = auto()
    CANCELLED = auto()


class TimeoutHandler:
    """Timeout handler for time limiter

    You can extend this class to create your own handler,
    MySQLTimeoutHandler with _name="MySQL" for example.
    You can use cancel() method to cancel the call.

    Typical uses of this class take the following form:

        class MySQLTimeoutHandler(TimeoutHandler):
            timeout = 0.5

            def __init__(self):
                super(MySQLTimeoutHandler, self).__init__()
                # Some way to get MySQL thread id
                self.thread_id = 1

            def _run(self):
                # Kill MySQL connection
                print(self.thread_id)
    """

    timeout: float = None

    __slots__ = ["_state"]

    def __init__(self):
        self._state = TimeoutHandlerState.CREATED

    def run(self):
        if self.cancelled():
            return
        elif self._state in (
            TimeoutHandlerState.FAILED,
            TimeoutHandlerState.RUNNING,
            TimeoutHandlerState.DONE,
        ):
            raise RepetitiveScheduledException("Repetitive scheduler handler")

        try:
            self.running()
            self._run()
            self.done()
        except Exception as e:
            self.failed()
            raise e

    def _run(self):
        raise NotImplementedError

    def get_timeout(self) -> float:
        return self.timeout

    def done(self):
        if self._state == TimeoutHandlerState.RUNNING:
            self._state = TimeoutHandlerState.DONE

    def running(self):
        if self._state == TimeoutHandlerState.SCHEDULED:
            self._state = TimeoutHandlerState.RUNNING

    def failed(self):
        if self._state == TimeoutHandlerState.RUNNING:
            self._state = TimeoutHandlerState.FAILED

    def scheduled(self):
        if self._state == TimeoutHandlerState.CREATED:
            self._state = TimeoutHandlerState.SCHEDULED

    def cancel(self):
        if self._state in (
            TimeoutHandlerState.CREATED,
            TimeoutHandlerState.SCHEDULED,
        ):
            self._state = TimeoutHandlerState.CANCELLED

    def cancelled(self) -> bool:
        return self._state == TimeoutHandlerState.CANCELLED

    def __repr__(self):
        return f"TimeoutHandler[{self.timeout}s]"


def register_handler(handler: TimeoutHandler):
    """Register handler to scheduler
    """
    # Use event loop scheduler event
    from timelimiter.event_loop import event_loop_register

    event_loop_register(handler)


class TimeoutHandlerFactory:
    """Timeout handler factory to create handler
    """

    def create_handler(self) -> TimeoutHandler:
        raise NotImplementedError()
