import requests

url = "http://127.0.0.1:5000/items"
headers = {'Content-Type': 'application/json'}
data = {
    "name": "Example Item",
    "description": "This is a sample item.",
    "price": 19.99
}

response = requests.post(url, json=data, headers=headers)
print(response.json())