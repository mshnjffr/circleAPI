import requests 
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

def create_wallet_set_api(entity_secret_ciphertext, idempotency_key, name):
    url = "https://api.circle.com/v1/w3s/developer/walletSets"

    payload = {
        "entitySecretCiphertext": entity_secret_ciphertext,
        "idempotencyKey": idempotency_key,
        "name": name,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return f"Wallet already exists: {response.text}"
        elif response.status_code == 201:
            response_data = response.json()
            wallet_set_id = response_data.get("data", {}).get("walletSet", {}).get("id")
            if wallet_set_id:
                return f"Wallet created with ID: {wallet_set_id}"
            else:
                return "ID not found in the response"
        elif response.status_code == 400:
            return f"Bad request: {response.text}"
        elif response.status_code == 401:
            return f"Unauthorized: {response.text}"
        else:
            response.raise_for_status()

        # response.raise_for_status()  # Raise an exception for HTTP errors
        
        # # Parse the JSON response
        # response_data = response.json()
        # wallet_set_id = response_data.get("data", {}).get("walletSet", {}).get("id")

        # if wallet_set_id:
        #     return wallet_set_id
        # else:
        #     return "ID not found in the response"
    
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    

def create_wallet_api(entity_secret_ciphertext, idempotency_key, wallet_set_id):
    url = "https://api.circle.com/v1/w3s/developer/wallets"

    payload = {
        "idempotencyKey": idempotency_key,
        "accountType": "SCA",
        "blockchains": ["MATIC-AMOY"],
        "count": 2,
        "entitySecretCiphertext": entity_secret_ciphertext,
        "walletSetId": wallet_set_id,
        "metadata": [
        {
            "name": "wallet-1",
            "refId": "w-1"
        },
        {
            "name": "wallet-2",
            "refId": "w-2"
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400:
            return f"Bad request: {response.text}"
        elif response.status_code == 401:
            return f"Unauthorized: {response.text}"
        else:
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    

def check_balance_api(wallet_id):
    url = f"https://api.circle.com/v1/w3s/wallets/{wallet_id}/balances"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        response_data = response.json()
        token_balances = response_data.get("data", {}).get("tokenBalances", [])
        
        if token_balances:
            first_token_id = token_balances[1].get("token", {}).get("id")
            return first_token_id
        return token_balances
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"

def create_transfer_transaction_api(entity_secret_ciphertext, idempotency_key, token_id, wallet_id):
    url = f"https://api.circle.com/v1/w3s/developer/transactions/transfer"

    payload = {
        "amounts": ["2"],
        "idempotencyKey": idempotency_key,
        "destinationAddress": "0xd5e7839447562767bb1bcaa9a78c0ce23226293a",
        "entitySecretCiphertext": entity_secret_ciphertext,
        "feeLevel": "LOW",
        # "blockchain": "MATIC-AMOY",
        "tokenId": token_id,
        "walletId": wallet_id
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
