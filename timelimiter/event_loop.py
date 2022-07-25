import asyncio
import functools
import threading
from asyncio import Handle

from timelimiter.timeout_handler import TimeoutHandler, TOTAL_HANDLER_COUNT

default_loop = asyncio.new_event_loop()


def schedule_handler(handler: TimeoutHandler):
    """Add handler to event loop
    """

    def event_wrapper():
        try:
            handler.run()
        finally:
            # Decrease handler count after handler run.
            TOTAL_HANDLER_COUNT.dec()

    # Increase handler count before add handler to event loop.
    TOTAL_HANDLER_COUNT.inc()
    default_loop.call_later(handler.get_timeout(), event_wrapper)
    handler.scheduled()


def run_loop(loop):
    """Set loop to current event loop and run forever
    """
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_loop():
    """Start a daemon thread to run event loop
    """
    print("Start run loop thread")
    threading.Thread(
        name="time-limiter-eventloop",
        target=lambda: run_loop(default_loop),
        daemon=True,
    ).start()


def event_loop_register(handler: TimeoutHandler):
    """Register event to event loop scheduler
    """
    default_loop.call_soon_threadsafe(
        functools.partial(schedule_handler, handler)
    )


def is_loop_running() -> bool:
    return default_loop.is_running()
