from rest_framework import serializers

from EndUserManagement.models import Case


#
# def checkStatus(value):
#     availableStatuses = [
#         "OPEN"
#     ]
#     if value not in availableStatuses:
#         raise serializers.ValidationError("The given status is not valid!")
#
# def createCaseValidator(role='EndUser'):
#     if role == 'EndUser':
#         return CaseCreateValidatorEndUser
#     return CaseCreateValidatorAdmin


class CaseCreateValidator(serializers.ModelSerializer):
    # User ID is required for the end users as a case creation filter and it should be the User ID of the logged in user
    # User = serializers.IntegerField()
    # Description = serializers.CharField(max_length=255, default=None)
    # Status = serializers.CharField(max_length=20, default=None, validators=[checkStatus])

    class Meta:
        model = Case
        fields = ['User', 'Description', 'Status']

#
# class CaseCreateValidatorAdmin(CaseCreateValidatorEndUser):
#     # User ID is not required for the admins as a case create filter
#     User = serializers.IntegerField(default=None)