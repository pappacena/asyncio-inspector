import asyncio
import pytest

from asyncio_inspector import enable_inpection


async def do_nothing():
    asyncio.sleep(0)
    return 1


def test_patch_event_loop_works():
    loop = asyncio.get_event_loop()
    with enable_inpection(loop):
        handler = loop.call_soon(do_nothing)
        assert handler._inspector_enabled
