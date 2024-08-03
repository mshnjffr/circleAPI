import base64
import codecs
from dotenv import load_dotenv
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

def encrypt_entity_secret(public_key_string, hex_encoded_entity_secret):


    entity_secret = bytes.fromhex(hex_encoded_entity_secret)

    if len(entity_secret) != 32:
        raise ValueError("Invalid entity secret")

    public_key = RSA.importKey(public_key_string)

    # Encrypt data using the public key
    cipher_rsa = PKCS1_OAEP.new(key=public_key, hashAlgo=SHA256)
    encrypted_data = cipher_rsa.encrypt(entity_secret)

    # Encode to base64
    encrypted_data_base64 = base64.b64encode(encrypted_data)
    return encrypted_data_base64.decode()