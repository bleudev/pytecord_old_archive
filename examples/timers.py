from pytecord import Client

client = Client('YOUR_TOKEN')

@client.timer(seconds=1)
async def message_every_second():
    print("I'll send this message to your console every 1 second!")

@client.timer(days=1)
async def good_morning():
    print('Good morning!')

client.run()
