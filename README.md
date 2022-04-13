# Dispy
![alt text](https://img.shields.io/badge/version-0.1_dev_preview_2-informational?style=flat) ![alt text](https://img.shields.io/badge/lang-python-informational) ![alt text](https://img.shields.io/badge/minimal_python_version-3.8-informational)
## Using

### Creating and running bot

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", prefix="!")

bot.run()
```

### bot.on("ready")

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", prefix="!")


@bot.on("ready")
async def on_ready():
    print("Ready!")


bot.run()
```

