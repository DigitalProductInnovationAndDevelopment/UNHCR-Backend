from rest_framework import serializers

from EndUserManagement.models import CaseCreateFeedback

from . import CustomModelSerializer

class CaseCreateFeedbackCreateValidator(CustomModelSerializer):
    class Meta:
        model = CaseCreateFeedback
        # Case is not required because case ID will come as a path parameter
        exclude = ['ID', 'Case']