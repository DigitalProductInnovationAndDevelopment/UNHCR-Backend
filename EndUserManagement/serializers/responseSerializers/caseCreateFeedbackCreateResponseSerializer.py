from rest_framework import serializers

from EndUserManagement.models import CaseCreateFeedback

class CaseCreateFeedbackCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseCreateFeedback
        fields = '__all__'