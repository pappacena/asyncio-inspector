---
# asyncio_inspector

[![codecov](https://codecov.io/gh/pappacena/asyncio-inspector/branch/main/graph/badge.svg?token=asyncio-inspector_token_here)](https://codecov.io/gh/pappacena/asyncio-inspector)
[![CI](https://github.com/pappacena/asyncio-inspector/actions/workflows/main.yml/badge.svg)](https://github.com/pappacena/asyncio-inspector/actions/workflows/main.yml)

Crazily simple statistics tracker for asyncio event loops, for the moments when just setting the event loop to debug mode is not enough.

This package is meant to be used to track basic statistics about asyncio event loops, so you can easily see which methods are blocking the event loop for longer, preventing other tasks from running.

## Install it from PyPI

```bash
pip install asyncio_inspector
```

## Usage

Enable inspection on any given event loop with the `inspect(event_loop)` and `uninspect(event_loop)` methods:


```py
from asyncio_inspector import inspect, uninspect

loop = asyncio.get_event_loop()
stats_tracker = inspect(loop)
loop.call_soon(my_async_function)
loop.call_soon(another_async_function)
loop.call_soon(loop.stop)

uninspect(loop)
```

Or with a context manager:

```py
loop = asyncio.get_event_loop()
with enable_inpection(loop) as stats_tracker:
    await my_async_function()
    await another_async_function()
```

Then, you will have some statistics in the stats_tracker object:

```py
stats_tracker.call_counts == {
    "my_async_function": 1,
    "another_async_function": 1
}

# Times are in nanosecs
stats_tracker.total_time == {
    "my_async_function": 123,
    "another_async_function": 333
}

stats_tracker.max_time == {
    "my_async_function": 400,
    "another_async_function": 500
}

stats_tracker.min_time == {
    "my_async_function": 100,
    "another_async_function": 200
}
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
