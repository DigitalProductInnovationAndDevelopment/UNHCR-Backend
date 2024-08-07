from rest_framework import serializers

from EndUserManagement.models import User

from . import CustomModelSerializer

class AdminUserUpdateValidator(CustomModelSerializer):
    class Meta:
        model = User
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False