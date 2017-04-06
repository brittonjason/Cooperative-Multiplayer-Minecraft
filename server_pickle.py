import pickle
import json


def server_pickle(x, y, z, token):
	data = {{"x":x, "y":y, "z":z}, {"token":token}}
	return pickle.dumps(json.dumps(data))

def server_unpickle(pickled_data):
	unpickled_data = json.loads(pickle.loads(pickled_data.decode("utf-8")))
	return [unpickled_data["player_id"], unpickled_data["x"], unpickled_data["y"], unpickled_data["z"], unpickled_data["block_type"]] 
