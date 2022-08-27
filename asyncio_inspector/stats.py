from typing import Optional

from sortedcollections import ValueSortedDict

from asyncio_inspector.events import ObservableDeque, ObservableHandle


def invert(x):
    return -x


class BaseStatsTracker:
    """"Basic stats tracker""" ""

    ready_queue: Optional[ObservableDeque]
    call_counts: ValueSortedDict
    total_time: ValueSortedDict
    avg_time: ValueSortedDict
    max_time: ValueSortedDict
    min_time: ValueSortedDict

    def __init__(self, ready_queue: ObservableDeque = None) -> None:
        self.ready_queue = ready_queue
        self.call_counts = ValueSortedDict(invert)
        self.total_time = ValueSortedDict(invert)
        self.avg_time = ValueSortedDict(invert)
        self.max_time = ValueSortedDict(invert)
        self.min_time = ValueSortedDict(invert)

    def track_call(
        self,
        identifier: str,
        start_timestamp: int,
        end_timestamp: int,
    ) -> None:
        if identifier not in self.call_counts:
            self.call_counts[identifier] = 0
            self.total_time[identifier] = 0
            self.avg_time[identifier] = 0
            self.max_time[identifier] = 0
            self.min_time[identifier] = 0

        self.call_counts[identifier] += 1
        elapsed_time = end_timestamp - start_timestamp
        self.total_time[identifier] += elapsed_time
        if elapsed_time > self.max_time[identifier]:
            self.max_time[identifier] = elapsed_time
        if elapsed_time < self.min_time[identifier]:
            self.min_time[identifier] = elapsed_time
        self.avg_time[identifier] = (
            self.total_time[identifier] / self.call_counts[identifier]
        )
