from pytecord import Client

client = Client('YOUR_TOKEN')

@client.listen()
async def ready():
    print("Hello, i'm bot!")

client.run()
