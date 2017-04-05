import asyncio
from aiocoap import *

run = asyncio.get_event_loop().run_until_complete

async def getPlayerPos():
	protocol = await Context.create_client_context()
	msg = Message(code=GET, uri="coap://localhost/minecraft/position")
	response = await protocol.request(msg).response
	print(response.payload)

while True:
	cmd_prompt = input('Get position? [y/n] ')

	if cmd_prompt == 'y' or cmd_prompt == 'Y':
		run(getPlayerPos())