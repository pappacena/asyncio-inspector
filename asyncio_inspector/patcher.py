from asyncio import AbstractEventLoop
from collections import deque
from contextlib import contextmanager

from asyncio_inspector.events import ObservableDeque
from asyncio_inspector.stats import BaseStatsTracker


def patch_event_loop_handler_creator(event_loop: AbstractEventLoop, stats_tracker: BaseStatsTracker) -> None:
    obs_deque = ObservableDeque(event_loop._ready)
    obs_deque.stats_tracker = stats_tracker
    event_loop._ready = obs_deque


def unpatch_event_loop_handler_creator(event_loop: AbstractEventLoop) -> None:
    event_loop._ready = deque(event_loop._ready)


@contextmanager
def enable_inpection(event_loop: AbstractEventLoop, stats_tracker=None) -> BaseStatsTracker:
    """Patches the given event loop to enable inspection."""
    if stats_tracker is None:
        stats_tracker = BaseStatsTracker()
    patch_event_loop_handler_creator(event_loop, stats_tracker)
    yield stats_tracker
    unpatch_event_loop_handler_creator(event_loop)