"""
`modals.py`

In this file you will learn to create a modals in disspy!

Enjoy!
"""

# Create a client
from disspy_v2 import Client
client = Client(token='token')

# Create a command
from disspy_v2 import app

# note: also you must import ui module
from disspy_v2 import ui

@client.command()
async def modals(ctx: app.Context):
    """
    An example modal in disspy!
    """
    # You have to inherit ui.Modal class to create a modal 
    class MyModal(ui.Modal, title='Feedback', custom_id='feedback'): # note: `custom_id` is not visible in discord
        inputs = [
            ui.TextInput(
                custom_id='rate', # unique string that not visible in discord
                label='Rate our bot from 1 to 9',
                style=ui.TextInputStyle.short,
                length=(1,1), # This means that user can input only 1-character message
                required=True,
                placeholder='1-9'
            ),
            ui.TextInput(
                custom_id='additional_feedback', # unique string that not visible in discord
                label='Additional feedback',
                style=ui.TextInputStyle.paragraph,
                length=(0, 1000), # This means that user can input 1000 characters maxium, 0 characters minimum
                required=False,
                placeholder='Please add /ban command!! :)'
            )
        ]
        async def submit(self, ctx: app.Context, rate: str, additional_feedback: str = ''): # Calls then user will click 
            await ctx.send_message('Thank you for your feedback!',
                                   'Your message:',
                                   f'Rate: {rate}',
                                   f'Additional feedback: {additional_feedback}',
                                   sep='\n',
                                   ephemeral=True)
    
    await ctx.send_modal(MyModal()) # Send this modal

# Run the client
client.run()
