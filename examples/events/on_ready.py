import disspy

bot = disspy.Client(token="TOKEN")  # Create bot

# On ready event

# on_ready()
@bot.on_ready()
async def on_ready():
    print("Logged as", bot.user.fullname)  # For example "Logged as Dispy#0000"

# event()
@bot.event()
async def ready():
    print("Logged as", bot.user.fullname)  # For example "Logged as Dispy#0000"

bot.run()  # Running bot
