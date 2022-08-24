import time
from abc import ABCMeta, abstractmethod
from logging import Logger
from threading import Thread
from typing import Optional

from asyncio_inspector.stats import BaseStatsTracker


class BaseReporter(metaclass=ABCMeta):
    stats_tracker: Optional[BaseStatsTracker] = None

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class LoggerReporter(Thread, BaseReporter):
    """Reporter that returns"""

    logger: Logger
    running: bool
    sleep_period: int

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger
        self.running = True
        self.sleep_period = 1
        self.daemon = True

    def run(self) -> None:
        while self.running:
            if self.stats_tracker is None:
                time.sleep(self.sleep_period)
                continue
            self.logger.debug(f"Call counts: {self.stats_tracker.call_counts}")
            time.sleep(self.sleep_period)

    def start(self) -> None:
        super().start()

    def stop(self):
        self.running = False
