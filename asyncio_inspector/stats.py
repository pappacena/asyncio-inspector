from collections import defaultdict
from asyncio_inspector.events import ObservableHandle


class BaseStatsTracker:
    """"Basic stats tracker"""""
    def __init__(self) -> None:
        self.call_counts = defaultdict(int)

    def track_call(self, handle: ObservableHandle) -> None:
        self.call_counts[handle._callback] += 1