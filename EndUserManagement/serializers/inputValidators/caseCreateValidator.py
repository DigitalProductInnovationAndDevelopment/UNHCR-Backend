from rest_framework import serializers

from EndUserManagement.models import Case

class CaseCreateValidator(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['Description']