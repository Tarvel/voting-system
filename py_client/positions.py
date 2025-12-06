import requests


endpoint = "http://localhost:8002/api/positions/"

get_response = requests.get(endpoint)

print (get_response.json())