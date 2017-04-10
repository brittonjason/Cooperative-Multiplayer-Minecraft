import logging
import pickle
import json
import asyncio
import aiocoap.resource as resource
import aiocoap
from mcpi.minecraft import Minecraft
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.OUT) # player 1
GPIO.setup(33, GPIO.OUT) # player 2
GPIO.setup(31, GPIO.OUT) # player 3

player_turn = 1

GPIO.output(37, GPIO.HIGH)
GPIO.output(33, GPIO.LOW)
GPIO.output(31, GPIO.LOW)

mc = Minecraft.create()
mc.postToChat("Connected...")  # Posts to minecraft chat

startx, starty, startz = mc.player.getPos()
x = startx
y = starty
z = startz


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
        global player_turn, x, y, z
        print("\n\n\nTEST TEST")
        print("\n\n\n" + str(request.payload) + "\n\n\n")
        self.content = request.payload

        payload = server_unpickle(request.payload)

        x = payload[1]
        y = payload[2]
        z = payload[3]

        # Place block
        mc.setBlock(x, y, z, payload[4])

        # Update turn to next player
        if player_turn == 3:
            player_turn = 1
        else:
            player_turn += 1
            
        if player_turn == 1:
            GPIO.output(37, GPIO.HIGH)
            GPIO.output(33, GPIO.LOW)
            GPIO.output(31, GPIO.LOW)
        elif player_turn == 2:
            GPIO.output(37, GPIO.LOW)
            GPIO.output(33, GPIO.HIGH)
            GPIO.output(31, GPIO.LOW)
        elif player_turn == 3:
            GPIO.output(37, GPIO.LOW)
            GPIO.output(33, GPIO.LOW)
            GPIO.output(31, GPIO.HIGH)

        if x == startx + 10 and y == starty + 1:
            player_turn = 0

        # Check if row if finished
        if x == startx + 10:
            y += 1
            x -= 10

        payload = b"Message retrieved!"

        # payload is response to PUT request
        return aiocoap.Message(payload=payload)


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


def server_pickle(x, y, z, token):
    data = {"x": x, "y": y, "z": z, "token": token}
    return pickle.dumps(json.dumps(data))


def server_unpickle(pickled_data):
    unpickled_data = json.loads(pickle.loads(pickled_data))
    return [unpickled_data["player_id"], unpickled_data["x"], unpickled_data["y"], unpickled_data["z"],
            unpickled_data["block_type"]]


def main():
    try:
        # Resource tree creation
        root = resource.Site()

        # adds resource at localhost/minecraft/position
        root.add_resource(('minecraft', 'position'), SendPlayerPos())

        asyncio.Task(aiocoap.Context.create_server_context(root))

        asyncio.get_event_loop().run_forever()
    except:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
