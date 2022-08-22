import requests
import json

url = "http://127.0.0.1:5000/currency/UAH/review"

payload = json.dumps({"rating": 4, "comment": 'comment'})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
