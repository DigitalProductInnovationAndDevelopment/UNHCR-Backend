import base64

from UNHCR_Backend.services import EncryptionService

encryptionService = EncryptionService()

class MessageService:
    def encryptStringMessage(self, userField, stringMessage):
        if stringMessage:
            # Convert the string message to bytes
            messageBytes = stringMessage.encode('utf-8')
            # Encrypt the bytes using the encryption service
            encryptedBytes = encryptionService.encryptData(userField, messageBytes)     
            # Convert the encrypted bytes to a base64-encoded string for storage
            encryptedMessage = base64.urlsafe_b64encode(encryptedBytes).decode('utf-8')
            return encryptedMessage
        # If the string message is null or empty, return it
        else:
            return stringMessage
    
    def decryptStringMessage(self, userField, encryptedMessage):
        if encryptedMessage:
            # Convert the base64-encoded string back to bytes
            encryptedBytes = base64.urlsafe_b64decode(encryptedMessage.encode('utf-8'))
            # Decrypt the bytes using the encryption service
            decryptedBytes = encryptionService.decryptData(userField, encryptedBytes)
            # Convert the decrypted bytes back to a string
            decryptedMessage = decryptedBytes.decode('utf-8')
            return decryptedMessage
        # If the encrypted message is null or empty, return it
        else:
            return encryptedMessage