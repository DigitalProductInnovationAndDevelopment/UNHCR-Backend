from rest_framework import serializers

from EndUserManagement.models import Case

from . import CustomModelSerializer

class AdminCaseCreateValidator(CustomModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'