from generate_entity_secret import encrypt_entity_secret
from wallet import create_wallet_set_api, create_wallet_api, check_balance_api, create_transfer_transaction_api
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

public_key_string = os.getenv("public_key_string")
hex_encoded_entity_secret = os.getenv("hex_encoded_entity_secret")

def generate_idempotency_key():
    return str(uuid.uuid4())

def create_wallet_set(public_key_string, hex_encoded_entity_secret, name):
    print("Function - create_wallet_set")
    try:
        encrypted_secret = encrypt_entity_secret(public_key_string, hex_encoded_entity_secret)
        print("Encrypted entity secret:", encrypted_secret)
        idempotency_key = generate_idempotency_key()
        print("")
        print("Idempotency_key:", idempotency_key)
        response = create_wallet_set_api(encrypted_secret, idempotency_key, name)
        print("API response:", response)
        if "Wallet created with ID:" in response:
            wallet_set_id = response.split(": ")[1]
            return wallet_set_id
        return None
    except Exception as e:
        print(f"Error: {e}")

def create_wallet(public_key_string, hex_encoded_entity_secret, wallet_set_id):
    try:
        encrypted_secret = encrypt_entity_secret(public_key_string, hex_encoded_entity_secret)
        print("Encrypted entity secret:", encrypted_secret)
        idempotency_key = generate_idempotency_key()
        print("")
        print("Idempotency_key:", idempotency_key)
        response = create_wallet_api(encrypted_secret, idempotency_key, wallet_set_id)
        print("Create Wallet API response:", response)
        return response
    except Exception as e:
        print(f"Error: {e}")

def transfer_transaction(public_key_string, hex_encoded_entity_secret, token_id, wallet_id):
    try:
        encrypted_secret = encrypt_entity_secret(public_key_string, hex_encoded_entity_secret)
        print("Encrypted entity secret:", encrypted_secret)
        idempotency_key = generate_idempotency_key()
        print("")
        print("Idempotency_key:", idempotency_key)
        response = create_transfer_transaction_api(encrypted_secret, idempotency_key, token_id, wallet_id)
        print("Create transfer transaction API response:", response)
        return response
    except Exception as e:
        print(f"Error: {e}")

def main():
    try:
    #Create wallet set
        # name = "Test Wallet Set v2"
        # wallet_set_id = create_wallet_set(public_key_string, hex_encoded_entity_secret, name)
        # if wallet_set_id:
        #     print(f"Stored Wallet Set ID: {wallet_set_id}")
            
        #Create wallet
        #     wallet_response = create_wallet(public_key_string, hex_encoded_entity_secret, wallet_set_id)
        #     if wallet_response:
        #         print(f"Wallet creation response: {wallet_response}")

        wallet_id = 'd776032f-8120-527d-9c06-980e7a2dea5b'

        # #Check balance, retrieve token Id
        token_id = check_balance_api(wallet_id)
        if token_id:
            print(f"Token ID: {token_id}")
            #Transfer transaction 
        #     transfer_transaction(public_key_string, hex_encoded_entity_secret, token_id, wallet_id)
        else:
            print("No token balance available")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()