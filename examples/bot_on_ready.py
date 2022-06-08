import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0)  # Create bot


# "On ready" event
@bot.on(disspy.DisBotEventType.ON_READY())
async def on_ready():
    print("Logged as " + bot.user.fullname)  # For example "Logged as Dispy#0000"


bot.run()  # Running bot
