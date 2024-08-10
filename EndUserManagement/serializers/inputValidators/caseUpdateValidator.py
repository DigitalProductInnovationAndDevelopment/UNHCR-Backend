from rest_framework import serializers

from EndUserManagement.models import Case

from . import CustomModelSerializer
    
class CaseUpdateValidator(CustomModelSerializer):
    class Meta:
        model = Case
        # Since CaseTypes field is required by model definition, empty list submission not allowed by the serializer
        exclude = ['ID', 'User', 'Status', 'UpdatedAt', 'CreatedAt', 'VulnerabilityCategory', 'VulnerabilityScore']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False