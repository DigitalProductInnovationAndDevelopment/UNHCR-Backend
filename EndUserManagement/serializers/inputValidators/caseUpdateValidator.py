from rest_framework import serializers

from EndUserManagement.models import Case, User
    
class CaseUpdateValidator(serializers.ModelSerializer):
    class Meta:
        model = Case
        exclude = ['ID', 'User', 'Status', 'UpdatedAt', 'CreatedAt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CaseTypes should not be submitted as an empty list
        requiredFields = ['CaseTypes']
        for field in self.fields.values():
            if field.field_name not in requiredFields:
                field.required = False