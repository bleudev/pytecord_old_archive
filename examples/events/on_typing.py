import disspy

client = disspy.Client(token="TOKEN", flags=disspy.Flags.messages())  # Create bot


# On typing event
@client.event()
async def typing(info: disspy.TypingInfo):
    print(info.author.id)
    await info.channel.send("You started typing!")


client.run()  # Running bot
