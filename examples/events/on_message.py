import disspy

bot = disspy.DisBot(token="TOKEN", flags=disspy.DisFlags.messages())  # Create bot


# "On message create" event
@bot.on("messagec")
async def on_messagec(message: disspy.DisMessage):
    if message.content == "!help":
        await message.channel.send("Help command*")

# on_message()
@bot.on_message("create")
async def on_messagec(message: disspy.DisMessage):
    if message.content == "!help":
        await message.channel.send("Help command*")



# "On message update" event
@bot.on("messageu")
async def on_messageu(message: disspy.DisMessage):
    await message.reply("You updated this message!")

# on_message()
@bot.on_message("update")
async def on_messageu(message: disspy.DisMessage):
    await message.reply("You updated this message!")



# "On message delete" event
@bot.on("messaged")
async def on_messaged(e: disspy.MessageDeleteEvent):
    await e.channel.send("Message deleted!")

# on_message()
@bot.on_message("delete")
async def on_messaged(e: disspy.MessageDeleteEvent):
    await e.channel.send("Message deleted!")


bot.run()  # Running bot
