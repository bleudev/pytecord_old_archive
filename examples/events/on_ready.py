import disspy

client = disspy.Client(token="TOKEN")  # Create bot


# on_ready()
@client.on_ready()
async def ready():
    print("Logged as", client.user.fullname)  # For example "Logged as Dispy#0000"

# event()
@client.event()
async def ready():
    print("Logged as", client.user.fullname)  # For example "Logged as Dispy#0000"

client.run()  # Running bot
