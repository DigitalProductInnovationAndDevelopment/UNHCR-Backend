from rest_framework import serializers

from EndUserManagement.models import Message

class MessageCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['UpdatedAt']