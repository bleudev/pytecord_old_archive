import disspy

bot = disspy.Client(token="TOKEN", flags=disspy.DisFlags.messages())  # Create bot


# on_typing()
@bot.event()
async def on_typing(user: disspy.User, channel: disspy.Channel):  # or async def typing(...): ...
    print(user.id)
    await channel.send("You started typing!")


# on_dm_typing()
@bot.event()
async def on_dm_typing(user: disspy.User, channel: disspy.Channel):  # or async def dm_typing(...): ...
    print(user.id)
    print(channel.id)


bot.run()  # Running bot
