import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0, flags=disspy.DisFlags.reactions())  # Create bot


# "On reaction add" event
@bot.on(disspy.DisBotEventType.ON_REACTION)
async def on_reaction(reaction: disspy.DisReaction):
    print(reaction.user.fullname)


# "On reaction remove" event
@bot.on(disspy.DisBotEventType.ON_REACTIONR)
async def on_reactionr(reaction: disspy.DisRemovedReaction):
    print(reaction.emoji.unicode)


bot.run()  # Running bot
