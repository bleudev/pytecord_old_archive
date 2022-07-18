import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0, flags=disspy.DisFlags.messages())  # Create bot


# "On message create" event
@bot.on(disspy.DisBotEventType.ON_MESSAGEC)
async def on_messagec(message: disspy.DisMessage):
    if message.content == "!help":
        await message.channel.send("Help command*")


# "On message update" event
@bot.on(disspy.DisBotEventType.ON_MESSAGEU)
async def on_messageu(message: disspy.DisMessage):
    await message.reply("You updated this message!")


# "On message delete" event
@bot.on(disspy.DisBotEventType.ON_MESSAGED)
async def on_messaged(e: disspy.MessageDeleteEvent):
    await e.channel.send("Message deleted!")


bot.run()  # Running bot
