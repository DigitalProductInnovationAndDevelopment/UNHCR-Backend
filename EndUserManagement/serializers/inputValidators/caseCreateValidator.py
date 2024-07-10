from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from collections.abc import Iterable

from EndUserManagement.models import Case, CaseType, PsnType

class CaseCreateValidator(serializers.ModelSerializer):
    class Meta:
        model = Case
        # Status is not required because it will be OPEN initially
        # User is not required because it is always logged in user for the end user
        exclude = ['User', 'Status', 'UpdatedAt', 'CreatedAt']

    # This function makes the CaseTypes and PsnTypes values list if they are not.
    # Manyy to many field input should be a list of IDs as default for DRF serializers.
    def to_internal_value(self, data):
        if 'CaseTypes' in data and not isinstance(data['CaseTypes'], list):
            data['CaseTypes'] = [data['CaseTypes']]
        if 'PsnTypes' in data and not isinstance(data['PsnTypes'], list):
            data['PsnTypes'] = [data['PsnTypes']]
        return super(CaseCreateValidator, self).to_internal_value(data)