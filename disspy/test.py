from disspy.application_commands import Slash
from disspy.core import DisApi

token = "OTY1NjY2MjcwNTAwNDk1Mzkw.Yl2gzA.bL6WiDnr-WMJPpdg-8gBA5rLy44"
# application_id = 965666270500495390

# print(Slash(token, application_id).register("test", "Hello"))
# print(Slash(token, application_id).getall())

async def on_ready():
    print("Ready!")

async def on_messagec(message):
    print("Wow! Message!")

async def on_register():
    pass

api = DisApi(token)
api.run(10, 512, "dnd", on_ready, on_messagec, on_register)
