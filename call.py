import json
import requests

url = 'http://127.0.0.1:5000/classify'

data={"Link":"https://scx2.b-cdn.net/gfx/news/hires/2019/water.jpg"}

data = json.dumps(data)

send_request = requests.post(url, data)
print(send_request)

print(send_request.text)