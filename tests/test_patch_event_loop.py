import asyncio
import pytest

from asyncio_inspector import enable_inpection


async def do_nothing():
    await asyncio.sleep(0)
    return 1


def test_patch_event_loop_works():
    loop = asyncio.get_event_loop()
    with enable_inpection(loop) as stats_tracker:
        loop.call_soon(do_nothing)
        loop.call_soon(loop.stop)
        loop.run_forever()
    assert stats_tracker.calls_count
