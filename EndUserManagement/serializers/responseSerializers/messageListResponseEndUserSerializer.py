from rest_framework import serializers

from EndUserManagement.models import Message
from EndUserManagement.models.Media import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'  # or specify the fields you want to include
def createMessageListResponseEndUserSerializer(role = 'EndUser'):
    if role == 'EndUser':
        return MessageListResponseEndUserSerializer
    return MessageListResponseAdminSerializer
    

class MessageListResponseEndUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

    Media = MediaSerializer()

class MessageListResponseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'