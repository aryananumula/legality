import json
from time import time

import requests

json_data = {"content": "What is the consensus on abortion?"}

start_time = time()

# iterable response
r = requests.post(
    "http://127.0.0.1:5000/session", json=json_data, stream=True
).iter_content(100000)
for chunk in r:
    if chunk:
        # decode the chunk
        decoded_chunk = json.loads(chunk.decode("utf-8"))
        # print the decoded chunk
        session_id = decoded_chunk.get("session_id")
        print(decoded_chunk["response"], end="\n", flush=True)
json_data = {"session_id": session_id, "content": "What about Roe v. Wade?"}

r = requests.post(
    "http://127.0.0.1:5000/session", json=json_data, stream=True
).iter_content(100000)
for chunk in r:
    if chunk:
        # decode the chunk
        decoded_chunk = json.loads(chunk.decode("utf-8"))
        # print the decoded chunk
        session_id = decoded_chunk.get("session_id")
        print(decoded_chunk["response"], end="\n", flush=True)
