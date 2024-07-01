from rest_framework import serializers

from EndUserManagement.models import Case

class AdminCaseCreateValidator(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'