from rest_framework import serializers

from EndUserManagement.models import User

def createUserUpdateValidator(role = 'EndUser'):
    if role == 'EndUser':
        return UserUpdateValidatorEndUser
    return UserUpdateValidatorAdmin
    
class UserUpdateValidatorEndUser(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class UserUpdateValidatorAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False