# DRFUP | Making bot

## How to make readable bot?
### May may do this

```python
import disspy

bot = disspy.DisBot("TOKEN", "message")
```
but please write the names of these arguments before specifying the arguments (For example, `token=`)
This does code more readable!
### Do this

```python
import disspy

bot = disspy.DisBot(token="TOKEN", type="message")
```

## Running
Run the bot 1 times, without type status for bot

Don't do this!

```python
import disspy

bot = disspy.DisBot(token="TOKEN", type="message")

bot.run("dnd")
```
Do this!

```python
import disspy

bot = disspy.DisBot(token="TOKEN", type="message", status="dnd")

bot.run()
```