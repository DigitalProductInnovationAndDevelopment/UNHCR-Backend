from rest_framework import serializers

from AdminManagement.models import UserDevice

class AdminUserDeviceGetReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = '__all__'