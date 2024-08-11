from rest_framework import serializers

from EndUserManagement.models import Message, MessageMedia
from EndUserManagement.services import MessageService

messageService = MessageService()

class MessageMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMedia
        fields = ['ID']

class AdminMessageListResponseSerializer(serializers.ModelSerializer):
    Media = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['UpdatedAt', 'Case']

    def get_Media(self, obj):
        if obj.HasMedia:
            media = MessageMedia.objects.filter(Message = obj)
            return MessageMediaSerializer(media, many=True).data
        return []
    
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