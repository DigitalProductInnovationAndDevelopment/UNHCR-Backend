from rest_framework import serializers

from EndUserManagement.models import Case

class CaseListResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        exclude = ['User', 'UpdatedAt']