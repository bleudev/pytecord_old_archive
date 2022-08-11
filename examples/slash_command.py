import disspy

bot = disspy.DisBot(token="TOKEN", application_id=0)  # Create bot


# Example slash command
@bot.slash_command(name="Foo", description="Bar",
                   options=[disspy.Option(name="foo",
                                          description="bar",
                                          option_type=disspy.OptionType.STRING,
                                          required=True)])
async def foo(ctx: disspy.Context, args: disspy.OptionArgs):
    print(args.get_string("foo"))

    await ctx.send(args.get("foo"))

bot.run()  # Running bot
