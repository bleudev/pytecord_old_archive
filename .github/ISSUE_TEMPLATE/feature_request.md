---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: Feature request
assignees: ''

---

**For what thing this feature?**
Testing
**Ideal solution**
```python
@bot.command()
async def test(ctx):
    await ctx.send("Test!")
```
**Not ideal but cool colution**
```python
async def test(ctx):
    await ctx.send("Test!")
bot.add_command(test)
```
