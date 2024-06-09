from rest_framework import serializers

from EndUserManagement.models import User

class UserGetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'email', 'is_staff', 'is_active', 'date_joined', 'CreatedAt', 'UpdatedAt', 'groups', 'user_permissions']