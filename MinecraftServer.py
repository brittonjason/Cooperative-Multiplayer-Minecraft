import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

from mcpi.minecraft import Minecraft

player_turn = 1

mc = Minecraft.create()
mc.postToChat("Connected...")  # Posts to minecraft chat

startx, starty, startz = mc.player.getPos()
x, y, z = 0


class SendPlayerPos(resource.Resource):
    def __init__(self):
        super(SendPlayerPos, self).__init__()

    # function for GET request
    async def render_get(self, request):
        # Send x, y, z, and player_turn
        payload = server_pickle(x, y, z, player_turn)

        # payload sends current position of player
        # payload_string = "X: " + str(x) + "\nY: " + str(y) + "\nZ: " + str(z)
        # payload = payload_string.encode('ascii')

        return aiocoap.Message(payload=payload)

    # function for PUT request
    async def render_put(self, request):
        global player_turn
        # request.payload is the the position to place the block
        print("\n\n\n" + str(request.payload) + "\n\n\n")
        self.content = request.payload

        payload = server_unpickle(request.payload)

        # Place block


        # Update x y z to where the block was placed

        # Update turn to next player
        if player_turn == 3:
            player_turn = 1
        else:
            player_turn += 1

        # payload is response to PUT request
        payload = "something arbitrary".encode('ascii')
        return aiocoap.Message(payload=payload)


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():
    # Resource tree creation
    root = resource.Site()

    # adds resource at localhost/minecraft/position
    root.add_resource(('minecraft', 'position'), SendPlayerPos())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
