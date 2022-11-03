"""
Example slash commands
"""
import disspy
from disspy import app_commands, StrOption, IntOption

bot = disspy.Client(token="TOKEN")  # Create bot


# Example command without options
@bot.command()
@app_commands.describe("Test")
async def hello(ctx: disspy.Context):
    a = ""
    with open("hello.txt", "r", encoding="utf-8") as f:
        a = f.read()

    await ctx.respond(str(a))


# Example command with options
@bot.command()
@app_commands.describe("Example command")
@app_commands.options.describe(message=StrOption().description("Message").required(),
                               integer=IntOption().description("Integer for math operation"))
async def foo(ctx: disspy.Context, message: str, integer: int = None):
    if integer:
        await ctx.respond(message, integer + 2, sep=" | ")
    else:
        await ctx.respond(message)


# Example context menus
# Message context menu
@bot.context_menu()
async def info(ctx: disspy.Context, message: disspy.DisMessage):
    await ctx.respond(f"Content: {message.content}", f"Channel id: {message.channel.id}", f"Id: {message.id}")


# User context menu
@bot.context_menu()
async def fullname(ctx: disspy.Context, user: disspy.DisUser):
    await ctx.respond(user.fullname)

bot.run()  # Running bot
