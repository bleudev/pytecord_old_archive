from pytecord import Client, Message, MessageDeleteEvent

client = Client('YOUR_TOKEN')

@client.listen()
async def message_create(message: Message): # also you can use async def message():
    await message.reply(f'Hello, {message.author}!') # str(message.author) == message.author.mention

@client.listen()
async def message_update(message: Message):
    await message.reply('This message has been updated!')

@client.listen()
async def message_delete(event: MessageDeleteEvent):
    await event.channel.send('Message has been deleted in this channel!')

client.run()
