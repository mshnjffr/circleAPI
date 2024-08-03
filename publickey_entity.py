import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


url = "https://api.circle.com/v1/w3s/config/entity/publicKey"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {API_TOKEN}"
}

response = requests.get(url, headers=headers)
response_dict = response.json()

print(json.dumps(response_dict, indent=4))