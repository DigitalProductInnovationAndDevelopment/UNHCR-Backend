import os
import base64
import hashlib

from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self):
        self.fileAndMessageEncryptionSecretKey = os.environ.get('ENCRYPTION_SECRET_KEY', 'encryption-secret-key')

    def generateUniqueKey(self, userField):
        combinedKey = (self.fileAndMessageEncryptionSecretKey + userField).encode()
        hashKey = hashlib.sha256(combinedKey).digest()
        uniqueKey = base64.urlsafe_b64encode(hashKey[:32])
        return uniqueKey.decode('utf-8')

    # This function is designed to work with binary data
    def decryptData(self, userField, encryptedData):
        cipher = Fernet(self.generateUniqueKey(userField))
        decryptedData = cipher.decrypt(encryptedData)
        return decryptedData

    # This function is designed to work with binary data
    def encryptData(self, userField, rawData):
        cipher = Fernet(self.generateUniqueKey(userField))
        encryptedData = cipher.encrypt(rawData)
        return encryptedData