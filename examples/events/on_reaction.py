import disspy

bot = disspy.Client(token="TOKEN", flags=disspy.Flags.reactions())  # Create bot


# "On reaction add" event
@bot.on("reaction")
async def on_reaction(reaction: disspy.Reaction):
    print(reaction.user.fullname)


# event()
@bot.event()
async def on_reaction(reaction: disspy.Reaction):  # or async def reaction(...): ...
    print(reaction.user.fullname)


# "On reaction remove" event
@bot.on("reactionr")
async def on_reactionr(reaction: disspy.Reaction):
    print(reaction.emoji.unicode)


# event()
@bot.event()
async def on_reactionr(reaction: disspy.Reaction):  # or async def reactionr(...): ...
    print(reaction.emoji.unicode)

bot.run()  # Running bot
