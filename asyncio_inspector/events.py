import time
import weakref
from asyncio import Handle
from asyncio.tasks import Task
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio_inspector.stats import BaseStatsTracker


def get_callback_name(callback, frame=None):
    if frame is not None:
        return f"{frame.f_code.co_filename}:{frame.f_lineno}"
    # Check for TaskStepMethWrapper builtin type, which is used in
    # asyncio.run method to wrap the original coro.
    if hasattr(callback, "__self__") and hasattr(
            callback.__self__, "get_coro"
    ):return callback.__self__.get_coro().__qualname__
    elif hasattr(callback, "__qualname__"):
        return callback.__qualname__
    elif hasattr(callback, "__name__"):
        return callback.__name__
    else:
        # Last resource, just to make sure we track something
        return str(callback)


class ObservableCoro:
    __slots__ = ('coro', 'stats_tracker')

    def __init__(self, coro, stats_tracker):
        self.coro = coro
        self.stats_tracker = stats_tracker

    def send(self, *args, **kwargs):
        start = time.time_ns()
        try:
            self.coro.send(*args, **kwargs)
        finally:
            end = time.time_ns()
            self.stats_tracker.track_call(self, start, end)

    def get_callback(self):
        return get_callback_name(self.coro)

    def __getattribute__(self, item):
        if item in {'coro', 'send', 'stats_tracker', 'get_callback'}:
            return super(ObservableCoro, self).__getattribute__(item)
        return getattr(self.coro, item)


class ObservableTask(Task):
    __slots__ = ("stats_tracker",)

    def __init__(self, loop, coro, *, stats_tracker=None, name=None):
        obs_coro = ObservableCoro(coro, stats_tracker)
        super(ObservableTask, self).__init__(
            obs_coro,  # type: ignore
            loop=loop, name=name
        )
        self.stats_tracker = stats_tracker


class ObservableHandle(Handle):
    """Subclass of handle that enables observability"""

    __slots__ = ("stats_tracker",)

    stats_tracker: "BaseStatsTracker"

    @classmethod
    def from_handle(cls, obj: Handle, stats_tracker) -> "ObservableHandle":
        """"Creates a new ObservableHandle from the given Handle object""" ""
        obs_handle = cls.__new__(cls)
        attrs_to_copy = [
            i for i in Handle.__slots__ if i != "__weakref__"  # type: ignore
        ]
        for attr in attrs_to_copy:
            value = getattr(obj, attr)
            setattr(obs_handle, attr, value)
        obs_handle.stats_tracker = stats_tracker
        return obs_handle

    def _run(self, *args, **kwargs):
        """Executes the original handle, tracking statistics"""
        frame = None
        if (hasattr(self._callback, "__self__") and
                hasattr(self._callback.__self__, "get_coro")):
            frame = self._callback.__self__.get_coro().cr_frame
        identifier = get_callback_name(self._callback, frame=frame)

        start = time.time_ns()
        super(ObservableHandle, self)._run(*args, **kwargs)
        end = time.time_ns()
        self.stats_tracker.track_call(identifier, start, end)

    def get_callback(self) -> str:
        """"Returns the string representation of the callback""" ""
        callback = self._callback  # type: ignore
        return get_callback_name(callback)


class ObservableDeque(deque):
    """A deque of ObservableHandle"""

    __slots__ = ("stats_tracker",)

    def __init__(self, *args, **kwargs):
        super(ObservableDeque, self).__init__(*args, **kwargs)
        self.stats_tracker = None
    
    def append(self, handle):
        obs_handle = ObservableHandle.from_handle(handle, self.stats_tracker)
        super(ObservableDeque, self).append(obs_handle)
