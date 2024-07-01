from rest_framework import serializers

from EndUserManagement.models import Case, User
    
class AdminCaseUpdateValidator(serializers.ModelSerializer):
    class Meta:
        model = Case
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False