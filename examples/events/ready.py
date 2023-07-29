import pytecord

client = pytecord.Client('YOUR_TOKEN')

@client.listen('ready')
async def ready():
    print("Hello, i'm bot!")

client.run()