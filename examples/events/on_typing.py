import disspy

bot = disspy.DisBot(token="TOKEN", flags=disspy.DisFlags.messages())  # Create bot


# "On typing" event
@bot.on("typing")
async def on_typing(user: disspy.DisUser, channel: disspy.DisChannel):
    print(user.id)
    await channel.send("You started typing!")

# event()
@bot.event()
async def on_typing(user: disspy.DisUser, channel: disspy.DisChannel):  # or async def typing(...): ...
    print(user.id)
    await channel.send("You started typing!")



# "On dm typing" event
@bot.on("dm_typing")
async def on_dm_typing(user: disspy.DisUser, channel: disspy.DisDmChannel):
    print(user.id)
    print(channel.id)

# event()
@bot.event()
async def on_dm_typing(user: disspy.DisUser, channel: disspy.DisDmChannel):  # or async def dm_typing(...): ...
    print(user.id)
    print(channel.id)


bot.run()  # Running bot
