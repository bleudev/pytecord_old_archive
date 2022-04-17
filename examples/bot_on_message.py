import disspy

bot = disspy.DisBot(token="TOKEN", type=disspy.DisBotType.MESSAGE)  # Create bot

# "On message create" event
@bot.on(disspy.DisBotEventType.ON_MESSAGEC())
async def on_messagec(message: disspy.DisMessage):
    if message.content == "!help":
        await message.channel.send("Help command*")

bot.run()  # Running bot
