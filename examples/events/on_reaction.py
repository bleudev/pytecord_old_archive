import disspy

client = disspy.Client(token="TOKEN", flags=disspy.Flags.reactions())  # Create bot

# On reaction event
@client.event()
async def reaction(r: disspy.Reaction):
    print(r.user.fullname)


# On reaction remove event
@client.event()
async def reactionr(r: disspy.Reaction):
    print(r.emoji.unicode)

client.run()  # Running bot
