import disspy

bot = disspy.DisBot(token="TOKEN")  # Create bot


# on("ready")
@bot.on("ready")
async def on_ready():
    print("Logged as " + bot.user.fullname)  # For example "Logged as Dispy#0000"


# on_ready()
@bot.on_ready()
async def on_ready():
    print("Logged as " + bot.user.fullname)  # For example "Logged as Dispy#0000"

# event()
@bot.event()
async def on_ready():  # or async def ready(): ...
    print("Logged as " + bot.user.fullname)  # For example "Logged as Dispy#0000"

bot.run()  # Running bot
