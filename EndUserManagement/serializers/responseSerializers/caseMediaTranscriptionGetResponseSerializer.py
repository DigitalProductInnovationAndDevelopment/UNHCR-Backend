from rest_framework import serializers

from EndUserManagement.models import CaseMediaTranscription

class CaseMediaTranscriptionGetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseMediaTranscription
        fields = '__all__'