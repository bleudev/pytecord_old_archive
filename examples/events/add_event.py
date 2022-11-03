import disspy

bot = disspy.Client(token="TOKEN")  # Create bot


# add_event() example
async def on_ready():
    print("Hi")


bot.add_event("ready", on_ready)

bot.run()  # Running bot
