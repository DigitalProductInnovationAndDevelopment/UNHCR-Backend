from rest_framework import serializers

from EndUserManagement.models import Case

class CaseUpdateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        exclude = ['User', 'UpdatedAt', 'VulnerabilityCategory', 'VulnerabilityScore']