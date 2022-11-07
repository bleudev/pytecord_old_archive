import disspy

bot = disspy.Client(token="TOKEN", flags=disspy.Flags.reactions())  # Create bot

# On reaction event
@bot.event()
async def reaction(r: disspy.Reaction):
    print(r.user.fullname)


# On reaction remove event
@bot.event()
async def reactionr(r: disspy.Reaction):
    print(r.emoji.unicode)

bot.run()  # Running bot
