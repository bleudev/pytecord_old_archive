import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0, flags=disspy.DisFlags.messages())  # Create bot


# "On message create" event
@bot.on(disspy.DisBotEventType.ON_MESSAGEC)
async def on_messagec(message: disspy.DisMessage):
    if message.content == "!help":
        await message.channel.send("Help command*")

bot.run()  # Running bot
