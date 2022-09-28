#Client Side
import requests
URL="http://127.0.0.1:5000/weather"
response = requests.get(URL)
msg = response.json()
print(msg['data'])