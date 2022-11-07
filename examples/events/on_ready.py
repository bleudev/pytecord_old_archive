import disspy

client = disspy.Client(token="TOKEN")  # Create bot

# On ready event

# on_ready()
@client.on_ready()
async def on_ready():
    print("Logged as", client.user.fullname)  # For example "Logged as Dispy#0000"

# event()
@client.event()
async def ready():
    print("Logged as", client.user.fullname)  # For example "Logged as Dispy#0000"

client.run()  # Running bot
