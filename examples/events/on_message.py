import disspy

bot = disspy.Client(token="TOKEN", flags=disspy.Flags.messages())  # Create bot


# "On message create" event
@bot.event()
async def messagec(message: disspy.Message):
    if message.content == "!help":
        await message.channel.send("Help command*")

# on_message()
@bot.on_message("create")
async def messagec(message: disspy.Message):
    if message.content == "!help":
        await message.channel.send("Help command*")



# "On message update" event
@bot.event()
async def messageu(message: disspy.Message):
    await message.reply("You updated this message!")

# on_message()
@bot.on_message("update")
async def messageu(message: disspy.Message):
    await message.reply("You updated this message!")



# "On message delete" event
@bot.event()
async def messaged(e: disspy.RawMessage):
    await e.channel.send("Message deleted!")

# on_message()
@bot.on_message("delete")
async def messaged(e: disspy.RawMessage):
    await e.channel.send("Message deleted!")


bot.run()  # Running bot
