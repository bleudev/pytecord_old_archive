```python
class DisBot(token: str, status: Optional[str])
```
This class maked for create bot.

Atributues\
``
api: DisApi -> Api client with token of the bot
``\

``
token: str -> Token of bot
``\

``
application_id: int -> Application Id
``\

``
logger: Logger -> Bot logger with logs
``\

``
status: str -> Bot status in discord (ONLINE, IDLE, DND, INVISIBLE)
``\

``
user: DisUser -> Bot user
``\

``
isready: bool -> Bot is ready?
``\

``
intflags: int -> Int value of intents
``\