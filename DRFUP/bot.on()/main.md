# DRFUP | bot.on()

bot.on() is using for creating events for DisBot
(for example on_messagec() or on_ready())

Don't do this
```python
import disspy

bot = disspy.DisBot(token="TOKEN", status=disspy.DisBotStatus.DND)

async def messagec(message):
    await message.channel.send("Hi")

@bot.on("messagec")
async def on_messagec(message):
    await messagec(message)

bot.run()
```

Do this!
```python
import disspy

bot = disspy.DisBot(token="TOKEN", status=disspy.DisBotStatus.DND)

@bot.on("messagec")
async def on_messagec(message):
    await message.channel.send("Hi")

bot.run()
```
