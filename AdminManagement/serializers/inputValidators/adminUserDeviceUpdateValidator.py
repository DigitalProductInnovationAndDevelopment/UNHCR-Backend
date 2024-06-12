from rest_framework import serializers

from AdminManagement.models import UserDevice

class AdminUserDeviceUpdateValidator(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']
