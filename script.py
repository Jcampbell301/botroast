import requests
import json

resp = requests.get(
    'https://api.groupme.com/v3/groups?token=V55sFTJ6vv6kh9K5r9vtzgRjThs74sAOIFNVW4OL')

print(json.dumps(resp.json(), indent=4))
