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

    await ctx.respond(str(a))


# Example command with options
@bot.command()
@app_commands.describe("Bar")
@app_commands.options.describe(foo=StrOption().set_description("Foo").required(),
                               foo2=StrOption().set_description("Foo 2"))
async def foo(ctx: disspy.Context, foo: str, foo2: str = None):
    if foo2:
        await ctx.respond(f"{foo}\n{foo2}")
    else:
        await ctx.respond(foo)


# Example context menus
# Message context menu
@bot.context_menu()
async def info(ctx: disspy.Context, message: disspy.DisMessage):
    await ctx.respond(f"Content: {message.content}\nChannel id: {message.channel.id}\nId: {message.id}")


# User context menu
@bot.context_menu()
async def fullname(ctx: disspy.Context, user: disspy.DisUser):
    await ctx.respond(user.fullname)

bot.run()  # Running bot
