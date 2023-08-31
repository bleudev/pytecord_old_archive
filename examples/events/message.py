from pytecord import Client, Message

client = Client('YOUR_TOKEN')

@client.listen()
async def message_create(message: Message): # also you can use async def message():
    await message.reply(f'Hello, {message.author}!') # str(message.author) == message.author.mention

client.run()
