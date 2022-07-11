from unittest import TestCase

from timelimiter.exceptions import RepetitiveScheduledException
from timelimiter.timeout_handler import TimeoutHandler


class MySQLTimeoutHandler(TimeoutHandler):
    timeout = 0.5

    def __init__(self):
        super(MySQLTimeoutHandler, self).__init__()
        self.thread_id = 1

    def _run(self):
        pass


class MySQLTimeoutHandlerWithException(TimeoutHandler):
    timeout = 0.5

    def __init__(self):
        super(MySQLTimeoutHandlerWithException, self).__init__()
        self.thread_id = 1

    def _run(self):
        raise RuntimeError("Something wrong")


class TestTimeoutHandler(TestCase):
    def test_repetitive_run(self):
        handler = MySQLTimeoutHandler()
        with self.assertRaisesRegex(
            RepetitiveScheduledException, "Repetitive scheduler handler"
        ):
            handler.scheduled()

            handler.run()
            handler.run()

    def test_run_with_exception(self):
        handler = MySQLTimeoutHandlerWithException()
        with self.assertRaisesRegex(RuntimeError, "Something wrong"):
            handler.scheduled()
            handler.run()

