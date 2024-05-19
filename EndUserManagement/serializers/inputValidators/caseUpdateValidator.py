from rest_framework import serializers

from EndUserManagement.models import Case, User

def checkStatus(value):
    availableStatuses = [
        "OPEN",
        "VIEWED",
        "CW ASSIGNED",
        "ON PROGRESS",
        "CASE CLOSED"
    ]
    if value not in availableStatuses:
        raise serializers.ValidationError("The given status is not valid!")

def createCaseUpdateValidator(role = 'EndUser'):
    if role == 'EndUser':
        return CaseUpdateValidatorEndUser
    return CaseUpdateValidatorAdmin
    
class CaseUpdateValidatorEndUser(serializers.ModelSerializer):
    # Making Description required for now because there is only 1 field an end user can update
    Description = serializers.CharField(max_length = 255)
    
    class Meta:
        model = Case
        exclude = ['ID', 'User', 'Status', 'UpdatedAt', 'CreatedAt']

class CaseUpdateValidatorAdmin(serializers.ModelSerializer):
    # Only admin users can update the User ID and the status of a case
    Description = serializers.CharField(max_length = 255, required = False)
    User = serializers.IntegerField(required = False)
    Status = serializers.CharField(max_length = 20, validators = [checkStatus], required = False)

    class Meta:
        model = Case
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']

    def validate(self, data):
        """
        Runs after the default validation rules and the validators.
        """
        if "User" in data:
            try:
                newOwnerOfCase = User.objects.get(ID = data["User"])
                data["User"] = newOwnerOfCase
            except User.DoesNotExist as err:
                raise serializers.ValidationError("The given user is not valid.")
        return data
