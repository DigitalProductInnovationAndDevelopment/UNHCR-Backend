import base64
import hashlib

from cryptography.fernet import Fernet

secret_key = "JNQxTqQrhrrkmK_jc4IoN-JvMgsNQzFckgR-qDwSPpw="
def generate_unique_key(username, base_key):
    combined = (base_key + username).encode()
    hash_key = hashlib.sha256(combined).digest()
    unique_key = base64.urlsafe_b64encode(hash_key[:32])
    return unique_key.decode('utf-8')

def decrypt_data(user_field, encrypted_data):
    cipher = Fernet(generate_unique_key(user_field, secret_key))
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def encrypt_data(user_field, raw_data):
    cipher = Fernet(generate_unique_key(user_field, secret_key))
    encrypted_data = cipher.encrypt(raw_data)
    return encrypted_data

