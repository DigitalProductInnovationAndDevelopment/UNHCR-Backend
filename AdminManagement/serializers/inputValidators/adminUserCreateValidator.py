from rest_framework import serializers

from EndUserManagement.models import User

from . import CustomModelSerializer

class AdminUserCreateValidator(CustomModelSerializer):
    class Meta:
        model = User
        exclude = ['ID', 'CreatedAt', 'UpdatedAt']