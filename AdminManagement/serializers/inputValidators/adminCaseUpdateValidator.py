from rest_framework import serializers

from EndUserManagement.models import Case

from . import CustomModelSerializer
    
class AdminCaseUpdateValidator(CustomModelSerializer):
    class Meta:
        model = Case
        exclude = ['ID', 'UpdatedAt', 'CreatedAt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False