import requests
import json

url = "http://127.0.0.1:5000/currency/trade/UAH/USD"

payload = json.dumps({"amount": 10})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)