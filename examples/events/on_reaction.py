import disspy

bot = disspy.DisBot(token="TOKEN", flags=disspy.DisFlags.reactions())  # Create bot


# "On reaction add" event
@bot.on("reaction")
async def on_reaction(reaction: disspy.DisReaction):
    print(reaction.user.fullname)


# event()
@bot.event()
async def on_reaction(reaction: disspy.DisReaction):  # or async def reaction(...): ...
    print(reaction.user.fullname)


# "On reaction remove" event
@bot.on("reactionr")
async def on_reactionr(reaction: disspy.DisRemovedReaction):
    print(reaction.emoji.unicode)


# event()
@bot.event()
async def on_reactionr(reaction: disspy.DisRemovedReaction):  # or async def reactionr(...): ...
    print(reaction.emoji.unicode)

bot.run()  # Running bot
