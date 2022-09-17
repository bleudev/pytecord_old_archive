"""
Example slash commands
"""
import disspy
from disspy import app_commands, StrOption

bot = disspy.DisBot(token="TOKEN")  # Create bot


# Example command without options
@bot.command()
@app_commands.describe("Test")
async def hello(ctx: disspy.Context):
    a = ""
    with open("hello.txt", "r", encoding="utf-8") as f:
        a = f.read()

    await ctx.send(str(a))


# Example command with options
@bot.command()
@app_commands.describe("bar")
@app_commands.options.describe(foo=StrOption().set_description("bar").required())
async def foo(ctx: disspy.Context):
    a = ctx.args.get_string("foo")

    await ctx.send(a)


# Example context menus
# Message context menu
@bot.context_menu()
async def info(ctx: disspy.Context, message: disspy.DisMessage):
    await ctx.send(f"Content: {message.content}\nChannel id: {message.channel.id}\nId: {message.id}")


# User context menu
@bot.context_menu()
async def fullname(ctx: disspy.Context, user: disspy.DisUser):
    await ctx.send(user.fullname)

bot.run()  # Running bot
