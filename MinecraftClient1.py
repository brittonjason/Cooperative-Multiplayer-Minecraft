import asyncio
from aiocoap import *
import json
import pickle
import argparse
import time

run = asyncio.get_event_loop().run_until_complete

my_id = 1

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True, help='ip address of server')
args = parser.parse_args()

ip = args.i

unjson = ({})
x = 0
y = 0
z = 0
my_block_id = 1

# Function for GET request
async def getPlayerPos():
    global unjson, x, y, z
    protocol = await Context.create_client_context()
    msg = Message(code=GET, uri="coap://" + ip + "/minecraft/position")
    response = await protocol.request(msg).response
    unpickle = pickle.loads(response.payload)
    unjson = json.loads(unpickle)
    x = unjson["x"] + 1
    y = unjson["y"]
    z = unjson["z"]
    print(response.payload)


# Function for PUT request
async def putBlockPos():
    global x, y, z, my_block_id
    context = await Context.create_client_context()
    json_pos = json.dumps({"player_id": my_id, "x": x, "y": y, "z": z, "block_type": my_block_id})
    pickle_pos = pickle.dumps(json_pos)
    payload = pickle_pos  # payload to send to server. [x y z block_id]
    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = ip
    request.opt.uri_path = ("minecraft", "position")

    response = await context.request(request).response  # gets response from server
    print('Result: ' + str(response.payload))


while True:
    run(getPlayerPos())
    if unjson["token"] == my_id:
        run(putBlockPos())
    elif unjson["token"] == 0:
        break
    time.sleep(.4)
print("Wall is finished!")
