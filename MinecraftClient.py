import asyncio
from aiocoap import *
import json
import pickle
from time import sleep

run = asyncio.get_event_loop().run_until_complete

my_id = 1
my_block_type = 4

# Function for GET request
async def getPlayerPos():
	protocol = await Context.create_client_context()
	# change localhost to ip address
	msg = Message(code=GET, uri="coap://localhost/minecraft/position")
	response = await protocol.request(msg).response
	unpickle = pickle.loads(response.payload)
	unjson = json.loads(unpickle)
	x = unjson["x"] + 1
	y = unjson["y"]
	z = unjson["z"]
	print(response.payload)

# Function for PUT request
async def putBlockPos():
	context = await Context.create_client_context()
	json_pos = json.dumps({"player_id": my_id, "x": x, "y":y, "z":z, "block_type": my_block_id})
	pickle_pos = pickle.dumps(json_pos)
	payload = pickle_pos # payload to send to server. [x y z block_id]
	request = Message(code=PUT, payload=payload)
	# change localhost to ip address
	request.opt.uri_host = 'localhost'
	request.opt.uri_path = ("minecraft", "position")
	
	response = await context.request(request).response # gets response from server
	print('Result: ' + str(response.payload))

while True:
	getPlayerPos()
	if unjson["player_id"] == my_id:
		putBlockPos()
	elif unjson["player_id"] == 0:
		break
	time.sleep(1)
print("Wall is finished!")
