import asyncio
import platform
import time
from unittest import mock

from asyncio_inspector.patcher import enable_inpection
from asyncio_inspector.reporter import LoggerReporter


async def do_nothing() -> int:
    """Async function that only sleeps(0) and return"""
    await asyncio.sleep(0)
    return 1


def test_logger_reporter():
    logger = mock.Mock()

    loop = asyncio.get_event_loop()
    reporter = LoggerReporter(logger=logger)
    reporter.sleep_period = 0.1
    reporter.start()
    with enable_inpection(loop, reporter=reporter):
        for _ in range(5):
            loop.call_soon(do_nothing)
        loop.call_soon(loop.stop)
        loop.run_forever()

    # Wait at least 2x the sleep_period
    time.sleep(0.2)
    reporter.stop()

    # And make sure the reporter logged at least once
    assert logger.debug.call_count >= 1
    last_log_call = logger.debug.call_args_list[-1]
    msg = last_log_call.args[0]
    assert "'do_nothing': 5" in msg

    if platform.system() == "Windows":
        assert "Queue size: 1\n" in msg
    else:
        assert "Queue size: 0\n" in msg
