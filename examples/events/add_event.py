import disspy

client = disspy.Client(token="TOKEN")  # Create client


# add_event() example
async def on_ready():
    print("Hi")


client.add_event("ready", on_ready)

client.run()  # Running client
