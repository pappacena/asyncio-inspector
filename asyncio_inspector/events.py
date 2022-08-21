from asyncio import Handle, Task
from collections import deque
import time


class ObservableHandle(Handle):
    """Subclass of handle that enables observability"""
    __slots__ = ('stats_tracker', )

    @classmethod
    def from_handle(cls, obj: Handle, stats_tracker: 'BaseStatsTracker') -> 'ObservableDeque':
        """"Creates a new ObservableHandle from the given Handle object"""""
        obs_handle = cls.__new__(cls)
        attrs_to_copy = [
            i for i in Handle.__slots__ if i != '__weakref__'
        ]
        for attr in attrs_to_copy:
            value = getattr(obj, attr)
            setattr(obs_handle, attr, value)
        obs_handle.stats_tracker = stats_tracker
        return obs_handle

    def _run(self, *args, **kwargs):
        """Executes the original handle, tracking statistics"""
        start = time.time_ns()
        super(ObservableHandle, self)._run(*args, **kwargs)
        end = time.time_ns()
        self.stats_tracker.track_call(self, start, end)

    def get_callback(self):
        callback = self._callback
        # Check for TaskStepMethWrapper builtin type, which is used in
        # asyncio.run method to wrap the original coro.
        if hasattr(callback, '__self__') and hasattr(callback.__self__, 'get_coro'):
            callback = callback.__self__.get_coro().__qualname__
        else:
            callback = callback.__qualname__
        return callback


class ObservableDeque(deque):
    """A deque of ObservableHandle"""

    __slots__ = ('stats_tracker', )

    def __init__(self, *args, **kwargs):
        super(ObservableDeque, self).__init__(*args, **kwargs)
        self.stats_tracker = None

    def popleft(self, *args, **kwargs):
        handle = super(ObservableDeque, self).popleft(*args, **kwargs)
        return ObservableHandle.from_handle(handle, self.stats_tracker)
