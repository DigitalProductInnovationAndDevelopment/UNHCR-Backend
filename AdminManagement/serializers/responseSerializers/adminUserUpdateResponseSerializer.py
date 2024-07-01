from rest_framework import serializers

from EndUserManagement.models import User

class AdminUserUpdateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'