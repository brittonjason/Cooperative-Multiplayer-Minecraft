import asyncio
from aiocoap import *

run = asyncio.get_event_loop().run_until_complete

# Function for GET request
async def getPlayerPos():
	protocol = await Context.create_client_context()
	# change localhost to ip address
	msg = Message(code=GET, uri="coap://localhost/minecraft/position")
	response = await protocol.request(msg).response
	print(response.payload)

# Function for PUT request
async def putBlockPos():
	context = await Context.create_client_context()
	payload = b"[10 10 10 10]" # payload to send to server. [x y z block_id]
	request = Message(code=PUT, payload=payload)
	# change localhost to ip address
	request.opt.uri_host = 'localhost'
	request.opt.uri_path = ("minecraft", "position")
	
	response = await context.request(request).response # gets response from server
	print('Result: ' + str(response.payload))

while True:
	cmd_prompt = input('Get position? [y/n] ')

	if cmd_prompt == 'y' or cmd_prompt == 'Y':
		run(getPlayerPos())
	elif cmd_prompt == 'n' or cmd_prompt == 'N':
		run(putBlockPos())
