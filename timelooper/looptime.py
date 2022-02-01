import asyncio
from abc import abstractmethod, ABC
from datetime import timedelta


class Looped(ABC):
    @abstractmethod
    async def do(self) -> None:
        pass

    @abstractmethod
    def should_stop(self) -> bool:
        pass


async def loop_timed(action: Looped, interval: timedelta) -> None:
    timer = asyncio.create_task(asyncio.sleep(interval.total_seconds()))
    try:
        while not timer.done() and not action.should_stop():
            proc = asyncio.create_task(action.do())
            await asyncio.wait((proc, timer), return_when=asyncio.FIRST_COMPLETED)
            if not proc.done():
                proc.cancel()
            elif proc.exception():
                proc.result()
    finally:
        timer.cancel()
