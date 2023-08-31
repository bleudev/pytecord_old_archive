from typing import Literal

from datetime import datetime
from time import mktime

class Timestamp:
    @staticmethod
    def from_iso(timestamp: str) -> 'Timestamp':
        return Timestamp(datetime.fromisoformat(timestamp))
    
    @staticmethod
    def from_unix(unix_time: int) -> 'Timestamp':
        return Timestamp(datetime.fromtimestamp(unix_time))

    def __init__(self, timestamp: datetime = datetime.now()) -> None:
        self.__timestamp = timestamp

    def get(self) -> datetime:
        return self.__timestamp
    
    @property
    def second(self) -> int:
        return self.__timestamp.second
    
    @property
    def minute(self) -> int:
        return self.__timestamp.minute
    
    @property
    def hour(self) -> int:
        return self.__timestamp.hour
    
    @property
    def day(self) -> int:
        return self.__timestamp.day
    
    @property
    def month(self) -> int:
        return self.__timestamp.month
    
    @property
    def year(self) -> int:
        return self.__timestamp.year

    def to_unix(self) -> int:
        return int(mktime(self.__timestamp.timetuple()))
    
    def to_iso(self) -> str:
        return self.__timestamp.isoformat()

    def to_discord(self) -> str:
        return f'<t:{self.to_unix()}>'
    
    def to_tuple(self) -> tuple[int, ...]:
        return (self.year, self.month, self.day, self.hour, self.minute, self.second)
    
    def to_list(self) -> list[int]:
        return list(self.to_tuple())
    
    def to_dict(self) -> dict[Literal['year', 'month', 'day', 'hour', 'minute', 'second'], int]:
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'hour': self.hour,
            'minute': self.minute,
            'second': self.second
        }
    
    def __str__(self) -> str:
        return self.to_discord()

    def __int__(self) -> int:
        return self.to_unix()

    def __iter__(self):
        return self.to_tuple().__iter__()

    def __repr__(self) -> str:
        return self.to_discord()
