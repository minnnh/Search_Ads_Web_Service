import json
from pymemcache.client import base

# Replace with your Memcached server's host and port
host = '127.0.0.1'
port = 11212

# Connect to Memcached server
client = base.Client((host, port))

# Get all keys
keys = client.get(b'__all_keys__')

# If __all_keys__ doesn't exist, try to retrieve the keys one by one
if keys is None:
    keys = []
    for i in range(100):  # Assuming the maximum number of keys is 100
        key_bytes = client.get(f'__key_{i}')
        if key_bytes:
            key = key_bytes.decode('utf-8')
            keys.append(key)

# Limit to the first 100 keys
selected_keys = keys[:100]

# Retrieve values for the selected keys
data = {}
for key in selected_keys:
    value = client.get(key.encode('utf-8'))
    if value is not None:
        data[key] = value.decode('utf-8')

# Save to a JSON file
output_file = 'memcached_data.json'
with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(f"The first 100 items have been saved to {output_file}")

