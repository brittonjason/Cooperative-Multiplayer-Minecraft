import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

from mcpi.minecraft import Minecraft

player_count = 0

mc = Minecraft.create()
mc.postToChat("Connected...")

class SendPlayerPos(resource.Resource):
    """
    Example resource which supports GET method. It uses asyncio.sleep to
    simulate a long-running operation, and thus forces the protocol to send
    empty ACK first.
    """

    def __init__(self):
        super(SendPlayerPos, self).__init__()

    async def render_get(self, request):
		
        x, y, z = mc.player.getPos()
		
        payload_string = "X: " + str(x) + "\nY: " + str(y) + "\nZ: " + str(z)
		
        payload = payload_string.encode('ascii')
        return aiocoap.Message(payload=payload)
		
    async def render_put(self, request):
        print("\n\n\n" + str(request.payload) + "\n\n\n")
        self.content = request.payload
        payload = "something arbitrary".encode('ascii')
        return aiocoap.Message(payload=payload)
		

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('minecraft', 'position'), SendPlayerPos())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
