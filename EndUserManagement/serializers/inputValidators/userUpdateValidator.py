from rest_framework import serializers

from EndUserManagement.models import User

def createUserUpdateValidator(role = 'EndUser'):
    if role == 'EndUser':
        return UserUpdateValidatorEndUser
    return UserUpdateValidatorAdmin
    
class UserUpdateValidatorEndUser(serializers.ModelSerializer):
    # Making Description required for now because there is only 1 field an end user can update
    Description = serializers.CharField(max_length = 255)
    
    class Meta:
        model = User
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']

class UserUpdateValidatorAdmin(serializers.ModelSerializer):
    # Only admin users can update the User ID and the status of a case
    Description = serializers.CharField(max_length = 255, required = False)

    class Meta:
        model = User
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']

    def validate(self, data):
        """
        Runs after the default validation rules and the validators.
        """
        
        try:
            newOwnerOfCase = User.objects.get(ID = data["User"])
            data["User"] = newOwnerOfCase
        except User.DoesNotExist as err:
            raise serializers.ValidationError("The given user is not valid.")
        return data
