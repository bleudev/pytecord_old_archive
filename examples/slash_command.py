"""
Example slash commands
"""
import disspy

bot = disspy.DisBot(token="TOKEN")  # Create bot


# Example slash command without options
@bot.slash_command(name="hello", description="Test")
async def hello(ctx: disspy.Context):
    a = ""
    with open("hello.txt", "r", encoding="utf-8") as f:
        a = f.read()

    await ctx.send(str(a))


# Example slash command with options
@bot.slash_command(name="Foo", description="Bar",
                   options=[disspy.Option(name="foo",
                                          description="bar",
                                          option_type=disspy.OptionType.STRING,
                                          required=True)])
async def foo(ctx: disspy.Context):
    a = ctx.args.get_string("foo")

    await ctx.send(a)

bot.run()  # Running bot
