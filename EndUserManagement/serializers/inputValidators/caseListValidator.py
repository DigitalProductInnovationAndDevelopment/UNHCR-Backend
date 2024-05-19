from rest_framework import serializers

from EndUserManagement.models import Case

def checkDateOrder(value):
    if value not in ["asc", "desc", None]:
        raise serializers.ValidationError("The given date order is not valid!")
    
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

def createCaseListValidator(role = 'EndUser'):
    if role == 'EndUser':
        return CaseListValidatorEndUser
    return CaseListValidatorAdmin
    
class CaseListValidatorEndUser(serializers.ModelSerializer):
    # User ID is required for the end users as a case list filter and it should be the User ID of the logged in user
    User = serializers.IntegerField()
    Description = serializers.CharField(max_length = 255, default = None)
    Status = serializers.CharField(max_length = 20, default = None, validators = [checkStatus])
    CreatedAtOrder = serializers.CharField(default = None, validators = [checkDateOrder])
    UpdatedAtOrder = serializers.CharField(default = None, validators = [checkDateOrder])
    page = serializers.IntegerField(required = False)
    
    class Meta:
        model = Case
        exclude = ['ID', 'CreatedAt', 'UpdatedAt']

class CaseListValidatorAdmin(CaseListValidatorEndUser):
    # User ID is not required for the admins as a case list filter
    User = serializers.IntegerField(default = None)