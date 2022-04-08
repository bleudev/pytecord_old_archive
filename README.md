# Dispy
![alt text](https://img.shields.io/badge/version-0.2-informational?style=flat) ![alt text](https://img.shields.io/badge/lang-python-informational)
## Using

### Creating and running bot
```python
import dispy

bot = dispy.DisBot(token="YOUR_TOKEN", prefix="!")

bot.run()
```

### bot.on("ready")
```python
import dispy

bot = dispy.DisBot(token="YOUR_TOKEN", prefix="!")

@bot.on("ready")
async def on_ready():
    print("Ready!")

bot.run()
```

