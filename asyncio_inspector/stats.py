from collections import defaultdict
from typing import Dict, Optional

from asyncio_inspector.events import ObservableDeque, ObservableHandle


class BaseStatsTracker:
    """"Basic stats tracker""" ""

    ready_queue: Optional[ObservableDeque]
    call_counts: Dict[str, int]
    total_time: Dict[str, int]
    max_time: Dict[str, int]
    min_time: Dict[str, int]

    def __init__(self, ready_queue: ObservableDeque = None) -> None:
        self.ready_queue = ready_queue
        self.call_counts = defaultdict(int)
        self.total_time = defaultdict(int)
        self.max_time = defaultdict(int)
        self.min_time = defaultdict(int)

    def track_call(
        self,
        handle: ObservableHandle,
        start_timestamp: int,
        end_timestamp: int,
    ) -> None:
        callback = handle.get_callback()
        self.call_counts[callback] += 1
        elapsed_time = end_timestamp - start_timestamp
        self.total_time[callback] += elapsed_time
        if elapsed_time > self.max_time[callback]:
            self.max_time[callback] = elapsed_time
        if elapsed_time < self.min_time[callback]:
            self.min_time[callback] = elapsed_time
