from rest_framework import serializers

from EndUserManagement.models import User
    
class UserUpdateValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        # These fields should not be updated by the end user
        exclude = ['ID', 'password', 'last_login', 'is_superuser', 'email', 'is_staff', 'is_active', 'date_joined', 'CreatedAt', 'UpdatedAt', 'groups', 'user_permissions']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False