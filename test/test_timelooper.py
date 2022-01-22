import asyncio
from datetime import timedelta
from time import monotonic

import pytest

from timelooper.looptime import Looped, loop_timed


class LoopedDummy(Looped):
    def __init__(self, maxsize: int, sleep_time: float = 1.0):
        self.collected = []
        self.maxsize: int = maxsize
        self.sleep_time: float = sleep_time
        self.i = 0

    async def do(self) -> None:
        await asyncio.sleep(self.sleep_time)
        self.collected.append(self.i)
        self.i += 1

    def should_stop(self) -> bool:
        return len(self.collected) >= self.maxsize


@pytest.mark.asyncio
async def test_timelooper_breaks_on_time():
    looped = LoopedDummy(5)
    started_at = monotonic()
    await loop_timed(looped, timedelta(seconds=3.5))
    assert len(looped.collected) == 3
    assert 3.4 < monotonic() - started_at < 3.6


@pytest.mark.asyncio
async def test_timelooper_breaks_on_condition():
    looped = LoopedDummy(2)
    started_at = monotonic()
    await loop_timed(looped, timedelta(seconds=3.5))
    assert len(looped.collected) == 2
    assert 2 < monotonic() - started_at < 2.1


@pytest.mark.asyncio
async def test_timelooper_breaks_call_on_time():
    looped = LoopedDummy(10, 15.0)
    started_at = monotonic()
    await loop_timed(looped, timedelta(seconds=3.5))
    assert len(looped.collected) == 0
    assert 3.4 < monotonic() - started_at < 3.6
