## Timelooper

[![Build Status](https://app.travis-ci.com/monomonedula/timelooper.svg?branch=master)](https://app.travis-ci.com/monomonedula/timelooper)

I found myself re-implementing the same 
pattern over and over 
when it comes to repeating some task until 
some condition is met OR 
the time is up, so here it is abstracted and generalized into
a neat package. 

Yep, that's 25 lines of code + tests.


Here's a demo use case:
```python
from timelooper import Looped, loop_timed
from datetime import timedelta

# Suppose we are listening to some queue
#   and want to batch the incoming messages.
#   However, we only want to wait for
#   some limited time for a batch 
#   to be formed.


class CollectableBatch(Looped):
    def __init__(self, queue, maxsize):
        self.batch = []
        self._queue = queue
        self._maxsize = maxsize
    
    async def do(self) -> None:
        self.batch.append(await self._queue.get())

    def should_stop(self) -> bool:
        return len(self.batch) == self._maxsize

    
collected = CollectableBatch(queue, maxsize=10)
await loop_timed(collected, timedelta(seconds=30))  

print(collected.batch)  # or whatever

```


### Installation
```shell
pip install timelooper
```