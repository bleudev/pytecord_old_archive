import disspy
from disspy import app_commands

bot = disspy.DisBot(token="TOKEN")  # Create bot


# Buttons
@bot.command()
@app_commands.describe("Testing buttons")
async def button(ctx: disspy.Context):
    ar = disspy.ActionRow(bot)

    @ar.add(disspy.Button(label="Test", custom_id="test"))
    async def test(button_ctx: disspy.Context):
        await button_ctx.respond("You pressed a button!")

    await ctx.respond("Button", action_row=ar)


# Modal with TextInput
@bot.command()
@app_commands.describe("Show modal with text input")
async def text_input(ctx: disspy.Context):
    ar = disspy.ActionRow(bot)

    @ar.add(disspy.TextInput(label="name", min_length=1, max_length=100, placeholder="Max", required=True))
    async def test(input_ctx: disspy.Context, value: str):
        await input_ctx.respond(f"Hello, {value}")

    await ctx.send_modal(title="Enter your name", custom_id="name_input", action_row=ar)


# Select menu
@bot.command()
@app_commands.describe("Show message with select menu")
async def select_menu(ctx: disspy.Context):
    ar = disspy.ActionRow(bot)
    options = []

    options.append(disspy.SelectMenuOption(label="Moderator", description="person who is moderate users", value="moderator", emoji='😁'))
    options.append(disspy.SelectMenuOption(label="User", description="Just person", value="user", default=True, emoji='😎'))

    @ar.add(disspy.SelectMenu(custom_id="selectrole", options=options, placeholder="Owner", min_values=1, max_values=2))
    async def test(menu_ctx: disspy.Context, values: list):
        await menu_ctx.respond(str(values))

    await ctx.respond(content="Choice role", action_row=ar)

bot.run()  # Running bot
