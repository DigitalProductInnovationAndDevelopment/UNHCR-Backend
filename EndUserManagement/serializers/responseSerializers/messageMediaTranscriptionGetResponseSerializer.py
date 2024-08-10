from rest_framework import serializers

from EndUserManagement.models import MessageMediaTranscription

class MessageMediaTranscriptionGetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMediaTranscription
        fields = '__all__'