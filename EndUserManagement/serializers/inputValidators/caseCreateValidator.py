from rest_framework import serializers

from EndUserManagement.models import Case

class CaseCreateValidator(serializers.ModelSerializer):
    class Meta:
        model = Case
        # Status is not required because it will be OPEN initially
        # User is not required because it is always logged in user for the end user
        exclude = ['User', 'Status', 'UpdatedAt', 'CreatedAt']