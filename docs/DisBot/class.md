```python
class DisBot(token: Snowflake[str], application_id: Optional[Snowflake[int]],
             status: Optional[TypeOf(DisBotStatus)],
             flags: Optional[TypeOf(DisFlags)],
             debug: Optional[bool] = False,
             activity: Optional[Union[Activity, dict]])
```
This class maked for create bot.

Atributues:
name: type         |Description
-------------------|----------------------------------------------------
api: DisApi        |Api client with token of the bot
token: str         |Token of bot
application_id: int|Application id
logger: Logger     |Bot logger with logs
status: str        |Bot status in discord (ONLINE, IDLE, DND, INVISIBLE)
user: DisUser      |Bot user
isready: bool      |Bot is ready?
intflags: int      |Int value of intents