from rest_framework import serializers

from EndUserManagement.models import User

class UserCreateValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['ID', 'CreatedAt', 'UpdatedAt']