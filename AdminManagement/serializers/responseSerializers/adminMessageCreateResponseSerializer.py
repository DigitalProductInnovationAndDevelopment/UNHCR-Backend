from rest_framework import serializers

from EndUserManagement.models import Message
from EndUserManagement.services import MessageService

messageService = MessageService()

class AdminMessageCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['UpdatedAt']

    def to_representation(self, instance):
        """
        Decrypt the text_message field when retrieving.
        """
        representation = super().to_representation(instance)
        userField = instance.Case.User.EmailAddress
        encryptedTextMessage = representation['TextMessage']  
        # Decrypt the encrypted text message which is fetched from the DB
        representation['TextMessage'] = messageService.decryptStringMessage(userField, encryptedTextMessage)

        return representation