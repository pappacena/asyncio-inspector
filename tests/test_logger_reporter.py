import asyncio
import logging
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

    time.sleep(0.15)
    reporter.stop()

    assert logger.debug.call_count == 1
    msg = logger.debug.call_args[0][0]
    assert "'do_nothing': 5" in msg
