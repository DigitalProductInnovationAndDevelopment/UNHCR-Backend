from rest_framework import serializers

from EndUserManagement.models import Case

from . import CustomModelSerializer

def checkDateOrder(value):
    if value not in ["asc", "desc"]:
        raise serializers.ValidationError("The given date order is not valid!")
    
class CaseListValidator(CustomModelSerializer):
    CreatedAtOrder = serializers.CharField(validators = [checkDateOrder])
    UpdatedAtOrder = serializers.CharField(validators = [checkDateOrder])
    page = serializers.IntegerField(required = False)
    
    class Meta:
        model = Case
        exclude = ['ID', 'CreatedAt', 'UpdatedAt', 'User', 'VulnerabilityCategory', 'VulnerabilityScore']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False