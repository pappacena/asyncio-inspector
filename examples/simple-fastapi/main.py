import asyncio
import logging
import random
from time import sleep

import uvicorn
from fastapi import FastAPI

import asyncio_inspector
from asyncio_inspector.reporter import LoggerReporter

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    reporter = LoggerReporter(logger=logger)
    asyncio_inspector.inspect(loop, reporter=reporter)
    reporter.start()


async def potentially_slow_sync_operation():
    """Synchronously sleep between 1 and 5 secs"""
    sleep_time = random.random() * 5
    sleep(sleep_time)
    return sleep_time


@app.get("/")
async def read_root():
    slept = await potentially_slow_sync_operation()
    return {"Hello": f"World! Slept for {slept}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
