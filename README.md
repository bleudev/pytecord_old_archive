# Hi)
### Dispy - a package for creating bots in python.
This is mini doc for starting creating bots

## Creating bot
```python
import dispy

bot = dispy.DisBot("YOUR_TOKEN")
channel = bot.get_channel(id)
await channel.send("Test)")
```