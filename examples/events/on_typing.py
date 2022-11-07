import disspy

bot = disspy.Client(token="TOKEN", flags=disspy.Flags.messages())  # Create bot


# On typing event
@bot.event()
async def typing(info: disspy.TypingInfo):
    print(info.author.id)
    await info.channel.send("You started typing!")


bot.run()  # Running bot
