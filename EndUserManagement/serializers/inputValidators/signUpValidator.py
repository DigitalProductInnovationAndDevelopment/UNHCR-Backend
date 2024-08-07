from rest_framework import serializers

from EndUserManagement.models import User

from . import CustomModelSerializer

class SignUpValidator(CustomModelSerializer):
    Password = serializers.CharField(max_length = 20)

    class Meta:
        model = User
        exclude = ['ID', 'password', 'last_login', 'is_superuser', 'email', 'is_staff', 'is_active', 'date_joined', 'CreatedAt', 'UpdatedAt', 'groups', 'user_permissions']