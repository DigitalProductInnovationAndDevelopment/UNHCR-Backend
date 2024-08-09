from rest_framework import serializers

from AdminManagement.models import UserDevice

class AdminUserDeviceListResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = '__all__'