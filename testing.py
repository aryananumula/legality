from time import time

import requests

json_data = {"content": "What is the consensus on abortion?"}

start_time = time()

with requests.post(
    "http://127.0.0.1:5000/session", json=json_data, timeout=7, stream=True
) as r:
    print("Output:")
    for chunk in r.iter_lines(decode_unicode=True):
        if chunk:
            print(chunk, flush=True)  # Flush output immediately

end_time = time()

print("HTTP response time:", r.elapsed.total_seconds())
print("Actually elapsed time:", end_time - start_time)
