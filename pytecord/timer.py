from typing import Callable
from asyncio import create_task
from datetime import datetime
from time import mktime

class TimerLoop:
    def __init__(self, callable: Callable, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> None:
        self.callable = callable

        self.every_time = seconds
        self.every_time += minutes * 60
        self.every_time += hours * 60 * 60
        self.every_time += days * 60 * 60 * 24

    async def __thread(self):
        start_time = int(mktime(datetime.now().timetuple()))

        while True:
            time = int(mktime(datetime.now().timetuple()))

            if time - start_time >= self.every_time:
                start_time = int(mktime(datetime.now().timetuple()))

                await self.callable()


    def run(self):
        create_task(self.__thread())
