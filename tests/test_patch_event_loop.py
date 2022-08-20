import asyncio

from asyncio_inspector import enable_inpection, inspect, uninspect


async def do_nothing() -> int:
    await asyncio.sleep(0)
    return 1


def test_patch_even_loop():
    loop = asyncio.get_event_loop()
    try:
        stats_tracker = inspect(loop)
        loop.call_soon(do_nothing)
        loop.call_soon(loop.stop)
        loop.run_forever()
    finally:
        uninspect(loop)
    assert stats_tracker.call_counts == {do_nothing: 1, loop.stop: 1}


def test_patch_event_loop_context_manager():
    loop = asyncio.get_event_loop()
    with enable_inpection(loop) as stats_tracker:
        loop.call_soon(do_nothing)
        loop.call_soon(loop.stop)
        loop.run_forever()
    assert stats_tracker.call_counts == {do_nothing: 1, loop.stop: 1}
