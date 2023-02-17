import disspy

client = disspy.Client(token="TOKEN", flags=disspy.Flags.messages())  # Create bot


# "On message create" event
@client.event()
async def messagec(message: disspy.Message):
    if message.content == "!help":
        await message.channel.send("Help command*")

# on_message()
@client.on_message("create")
async def messagec(message: disspy.Message):
    if message.content == "!help":
        await message.channel.send("Help command*")



# "On message update" event
@client.event()
async def messageu(message: disspy.Message):
    await message.reply("You updated this message!")

# on_message()
@client.on_message("update")
async def messageu(message: disspy.Message):
    await message.reply("You updated this message!")



# "On message delete" event
@client.event()
async def messaged(message: disspy.RawMessage):
    await message.channel.send("Message deleted!")

# on_message()
@client.on_message("delete")
async def messaged(message: disspy.RawMessage):
    await message.channel.send("Message deleted!")

# DM messages

# "On dm message create" event
@client.event()
async def dmessagec(message: disspy.Message):
    if message.content == "!help":
        await message.channel.send("Help command*")

# on_dm_message()
@client.on_dm_message("create")
async def dmessagec(message: disspy.Message):
    if message.content == "!help":
        await message.channel.send("Help command*")



# "On dm message update" event
@client.event()
async def dmessageu(message: disspy.Message):
    await message.reply("You updated this message!")

# on_dm_message()
@client.on_dm_message("update")
async def dmessageu(message: disspy.Message):
    await message.reply("You updated this message!")



# "On dm message delete" event
@client.event()
async def dmessaged(message: disspy.RawMessage):
    await message.channel.send("Message deleted!")

# on_dm_message()
@client.on_dm_message("delete")
async def dmessaged(message: disspy.RawMessage):
    await message.channel.send("Message deleted!")

client.run()  # Running bot
