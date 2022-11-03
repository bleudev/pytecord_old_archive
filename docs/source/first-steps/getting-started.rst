Getting Started
###############

Contents:
    * `Install package`_
    * `Create bot in Discord`_
    * `Coding with disspy`_

Install package
***************

How to install disspy? Just type those lines in your command console

Windows::

    pip install -U disspy

Lunix::

    sudo pip install -U disspy

MacOs::

    python3 -m pip install -U disspy

Now you can follow to the next step

Create bot in Discord
*********************

To start creating bots, you need to create bot on
`official Discord Developer Portal <https://discord.com/developers/applications>`_

.. image:: images/1.png

Click "New application" button

.. image:: images/2.png

Come on with name and click "Create"

.. image:: images/3.png

Click "Bot" section

.. image:: images/4.png

Click "Add bot"

.. image:: images/5.png

Argee with warning

.. image:: images/6.png

Click "Reset token"

.. image:: images/7.png

Copy token

.. image:: images/8.png

Coding with disspy
******************

Now, let's write some code!

*Start creating your bot with the following code*::

    import disspy

    token = "YOUR_COPIED_TOKEN"

    bot = disspy.Client(token=token, application_id=application_id)  # You created bot!

Then, you can add any event using ``on() method``::

    @bot.on("ready")
    async def on_ready():
        print("Hi!")

This code prints "Hi!" when bot becomes ready in Discord Gateway

In end of the file you MUST type this line::

    bot.run()

This is very important because this method runs bot in Discord! 
Well... You are ready for coding with disspy.
