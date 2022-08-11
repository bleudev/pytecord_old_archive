import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0, flags=disspy.DisFlags.messages())  # Create bot


# "On typing" event
@bot.on(disspy.DisBotEventType.ON_TYPING)
async def on_typing(user: disspy.DisUser, channel: disspy.DisChannel):
    print(user.id)
    await channel.send("You started typing!")


# "On dm typing" event
@bot.on(disspy.DisBotEventType.ON_DM_TYPING)
async def on_dm_typing(user: disspy.DisUser, channel: disspy.DisDmChannel):
    print(user.id)
    print(channel.id)

bot.run()  # Running bot
