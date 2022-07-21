import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0)  # Create bot


# Buttons
@bot.slash_command(name="button", description="Testing buttons")
async def button(ctx: disspy.Context, args: disspy.OptionArgs):
    ar = disspy.ActionRow(bot)

    @ar.add(disspy.Button(label="Test", custom_id="test"))
    async def test(button_ctx: disspy.Context):
        await button_ctx.send("You pressed a button!")

    await ctx.send("Button", action_row=ar)


# Modal with TextInput
@bot.slash_command(name="text_input", description="Show modal with text input")
async def text_input(ctx: disspy.Context, args: disspy.OptionArgs):
    ar = disspy.ActionRow(bot)

    @ar.add(disspy.TextInput(label="name", min_length=1, max_length=100, placeholder="Max", required=True))
    async def test(input_ctx: disspy.Context, value: str):
        await input_ctx.send(content=f"Hello, {value}")

    await ctx.send_modal(title="Enter your name", custom_id="name_input", action_row=ar)


# Select menu
@bot.slash_command(name="select_menu", description="Show message with select menu")
async def select_menu(ctx: disspy.Context, args: disspy.OptionArgs):
    ar = disspy.ActionRow(bot)
    options = []

    options.append(disspy.SelectMenuOption(label="Moderator", description="person who is moderate users", value="moderator", emoji='😁'))
    options.append(disspy.SelectMenuOption(label="User", description="Just person", value="user", default=True, emoji='😎'))

    @ar.add(disspy.SelectMenu(custom_id="selectrole", options=options, placeholder="Owner", min_values=1, max_values=2))
    async def test(menu_ctx: disspy.Context, values: list[str]):
        await menu_ctx.send(content=str(values))

    await ctx.send(content="Choice role", action_row=ar)

bot.run()  # Running bot
