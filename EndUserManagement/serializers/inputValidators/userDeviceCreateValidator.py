from rest_framework import serializers
from AdminManagement.models import UserDevice

class UserDeviceCreateValidator(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        exclude = ['ID', 'CreatedAt', 'UpdatedAt']