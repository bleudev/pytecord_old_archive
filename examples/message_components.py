import disspy
from disspy import app_commands, TextInput, Button, SelectMenu, SelectMenuOption

client = disspy.Client(token="TOKEN")  # Create client


# Buttons
@client.command()
@app_commands.describe("Testing buttons")
async def test_button(ctx: disspy.Context):
    ar = disspy.ActionRow(client)

    @ar.add(Button(label="Test", custom_id="test"))
    async def test(button_ctx: disspy.Context):
        await button_ctx.respond("You pressed a button!")

    await ctx.respond("Button", action_row=ar)


# Modal with TextInput
@client.command()
@app_commands.describe("Say hello for you ;)")
async def say_hello(ctx: disspy.Context):
    ar = disspy.ActionRow(client)

    @ar.add(TextInput(label="name", min_length=1, max_length=100, placeholder="John", required=True))
    async def test(input_ctx: disspy.Context, value: str):
        await input_ctx.respond(f"Hello, {value}")

    await ctx.send_modal(title="Enter your name", custom_id="name_input", action_row=ar)


# Select menu
@client.command()
@app_commands.describe("Info about roles on server")
async def info_about_role(ctx: disspy.Context):
    ar = disspy.ActionRow(client)
    options = []

    options.append(SelectMenuOption(label="Moderator", description="Person who is moderate users", value="moderator", emoji='😎'))
    options.append(SelectMenuOption(label="User", description="Just person", value="user", default=True, emoji='😁'))

    @ar.add(SelectMenu(custom_id="selectrole", options=options, placeholder="Choose role", min_values=1, max_values=1))
    async def test(menu_ctx: disspy.Context, values: list):
        value = values[0]

        if value == "user":
            await menu_ctx.respond("User is person who just joined this server")
        elif value == "moderator":
            await menu_ctx.respond("Moderator is a person who is moderate this server for good chatting")

    await ctx.respond("Choose role for info", action_row=ar)

client.run()  # Running bot
