from rest_framework import serializers

from AdminManagement.models import UserDevice

class UserDeviceUpdateValidator(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        exclude = ['ID', 'UserID', 'UpdatedAt', 'CreatedAt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False